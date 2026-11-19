#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#


"""Tests for request options, response metadata, retries and the newer endpoints.

These run against a local HTTP server, so the retries of the real HTTP adapter are exercised.
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Iterator, List, Tuple
from urllib.parse import parse_qs, urlparse

import pytest
from generatorlabs import Client, Config
from generatorlabs.exception import Exception as GLException

OK = {"status_code": 200, "status_message": "OK"}


class ApiServer:
    """A local API that records each request and answers with the queued replies."""

    def __init__(self) -> None:
        self.requests: List[Dict[str, Any]] = []
        self.replies: List[Tuple[int, Dict[str, str], str]] = []

        api = self

        class Handler(BaseHTTPRequestHandler):
            def _handle(self) -> None:
                length = int(self.headers.get("Content-Length") or 0)
                url = urlparse(self.path)
                api.requests.append({
                    "method": self.command,
                    "path": url.path,
                    "query": parse_qs(url.query),
                    "body": parse_qs(self.rfile.read(length).decode()),
                    "headers": {k.lower(): v for k, v in self.headers.items()},
                })

                status, headers, body = api.replies.pop(0) if api.replies else (200, {}, json.dumps(OK))
                self.send_response(status)
                for name, value in headers.items():
                    self.send_header(name, value)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body.encode())

            do_GET = do_POST = do_PUT = do_DELETE = _handle

            def log_message(self, *args: Any) -> None:
                pass

        self.server = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def reply(self, status: int = 200, headers: Dict[str, str] = {}, body: Any = OK) -> None:
        self.replies.append((status, headers, body if isinstance(body, str) else json.dumps(body)))

    def client(self) -> Client:
        return Client("AC" + "a" * 32, "b" * 64, Config(
            base_url=f"http://127.0.0.1:{self.server.server_port}/4.0/",
            retry_backoff=0.01,
        ))


@pytest.fixture
def api() -> Iterator[ApiServer]:
    server = ApiServer()
    yield server
    server.server.shutdown()
    server.server.server_close()


class TestIdempotencyKey:
    """The Idempotency-Key of a request that creates something."""

    def test_same_key_on_every_retry(self, api: ApiServer) -> None:
        api.reply(500, body={"status_code": 500, "status_message": "Server error."})
        api.reply(200)

        api.client().rbl.hosts.create({"name": "Test", "host": "192.0.2.1"})

        assert len(api.requests) == 2
        key = api.requests[0]["headers"]["idempotency-key"]
        assert len(key) == 36
        assert api.requests[1]["headers"]["idempotency-key"] == key

    def test_new_key_for_each_call(self, api: ApiServer) -> None:
        client = api.client()
        client.rbl.hosts.create({"name": "One", "host": "192.0.2.1"})
        client.rbl.hosts.create({"name": "Two", "host": "192.0.2.2"})

        assert api.requests[0]["headers"]["idempotency-key"] != api.requests[1]["headers"]["idempotency-key"]

    def test_caller_key_wins(self, api: ApiServer) -> None:
        api.client().rbl.check.start({"host": "192.0.2.1"}, idempotency_key="my-key")

        assert api.requests[0]["headers"]["idempotency-key"] == "my-key"

    def test_key_on_the_endpoints_that_accept_one(self, api: ApiServer) -> None:
        client = api.client()
        client.contact.contacts.resend("COx")
        client.contact.contacts.confirm("COx", {"authcode": "1234"})
        client.cert.monitors.delete("CMx")
        client.cert.monitors.check("CMx")

        assert all("idempotency-key" in request["headers"] for request in api.requests)

    def test_no_key_on_other_writes(self, api: ApiServer) -> None:
        client = api.client()
        client.rbl.hosts.update("HTx", {"name": "Test"})
        client.rbl.hosts.pause("HTx")
        client.rbl.hosts.delete("HTx")

        assert all("idempotency-key" not in request["headers"] for request in api.requests)

    def test_replayed(self, api: ApiServer) -> None:
        api.reply(200, {"Idempotent-Replayed": "true"})
        api.reply(200)
        client = api.client()

        assert client.rbl.hosts.create({"name": "Test"}).replayed is True
        assert client.rbl.hosts.create({"name": "Test"}).replayed is False


class TestRequestOptions:
    """Request ids, conditional requests and field selection."""

    def test_request_id_sent_and_returned(self, api: ApiServer) -> None:
        api.reply(200, {"X-Request-Id": "req-1"})

        response = api.client().rbl.hosts.get(request_id="req-1")

        assert api.requests[0]["headers"]["x-request-id"] == "req-1"
        assert response.request_id == "req-1"

    def test_request_id_on_an_error(self, api: ApiServer) -> None:
        api.reply(404, {"X-Request-Id": "req-2"}, {"status_code": 404, "status_message": "Not found."})

        with pytest.raises(GLException) as exc:
            api.client().rbl.hosts.get("HTx")

        assert exc.value.status_code == 404
        assert exc.value.request_id == "req-2"

    def test_etag_and_not_modified(self, api: ApiServer) -> None:
        api.reply(200, {"ETag": 'W/"abc"'}, {**OK, "data": []})
        api.reply(304, {"ETag": 'W/"abc"'}, "")
        client = api.client()

        first = client.rbl.hosts.get()
        second = client.rbl.hosts.get(if_none_match=first.etag)

        assert first.etag == 'W/"abc"'
        assert first.not_modified is False
        assert api.requests[1]["headers"]["if-none-match"] == 'W/"abc"'
        assert second.not_modified is True
        assert len(second) == 0

    def test_fields_on_a_single_get(self, api: ApiServer) -> None:
        api.client().rbl.hosts.get("HTx", fields=["id", "host"])

        assert api.requests[0]["path"] == "/4.0/rbl/hosts/HTx.json"
        assert api.requests[0]["query"] == {"fields": ["id,host"]}

    def test_fields_on_a_list(self, api: ApiServer) -> None:
        api.client().rbl.hosts.get({"page": 2}, fields="id,host")

        assert api.requests[0]["query"] == {"page": ["2"], "fields": ["id,host"]}

    def test_unknown_option(self, api: ApiServer) -> None:
        with pytest.raises(GLException):
            api.client().rbl.hosts.get(bogus=1)

        assert len(api.requests) == 0


class TestRetryAfter:
    """The Retry-After header of a 429."""

    def test_short_wait_is_retried(self, api: ApiServer) -> None:
        api.reply(429, {"Retry-After": "1"}, {"status_code": 429, "status_message": "Slow down."})
        api.reply(200)

        api.client().rbl.hosts.get()

        assert len(api.requests) == 2

    def test_long_wait_is_returned_as_the_error(self, api: ApiServer) -> None:
        api.reply(429, {"Retry-After": "3600"}, {"status_code": 429, "status_message": "Slow down."})

        with pytest.raises(GLException) as exc:
            api.client().cert.monitors.check("CMx")

        assert exc.value.status_code == 429
        assert len(api.requests) == 1


class TestAccount:
    """The account endpoints."""

    def test_get(self, api: ApiServer) -> None:
        api.reply(200, body={**OK, "data": {"balance": 80.1226}})

        response = api.client().account.get()

        assert api.requests[0]["method"] == "GET"
        assert api.requests[0]["path"] == "/4.0/account.json"
        assert response["data"]["balance"] == 80.1226

    def test_balance(self, api: ApiServer) -> None:
        api.reply(200, {"Content-Type": "text/plain"}, "80.1226\n")

        assert api.client().account.balance() == 80.1226
        assert api.requests[0]["path"] == "/4.0/account/balance.json"

    def test_balance_error(self, api: ApiServer) -> None:
        api.reply(401, {"Content-Type": "text/plain"}, "-1\n")

        with pytest.raises(GLException) as exc:
            api.client().account.balance()

        assert exc.value.status_code == 401

    def test_usage(self, api: ApiServer) -> None:
        api.client().account.usage({"months": 3})

        assert api.requests[0]["path"] == "/4.0/account/usage.json"
        assert api.requests[0]["query"] == {"months": ["3"]}

    def test_pause_and_resume_checks(self, api: ApiServer) -> None:
        client = api.client()
        client.account.pause_checks()
        client.account.resume_checks()

        assert [(r["method"], r["path"]) for r in api.requests] == [
            ("POST", "/4.0/account/checks/pause.json"),
            ("POST", "/4.0/account/checks/resume.json"),
        ]


class TestCert:
    """The certificate findings, check and count endpoints."""

    def test_findings(self, api: ApiServer) -> None:
        api.client().cert.findings.get({"dismissed": 1})

        assert api.requests[0]["path"] == "/4.0/cert/findings.json"
        assert api.requests[0]["query"] == {"dismissed": ["1"]}

    def test_findings_get_all(self, api: ApiServer) -> None:
        api.reply(200, body={**OK, "total_pages": 2, "data": [{"id": "CM1"}]})
        api.reply(200, body={**OK, "total_pages": 2, "data": [{"id": "CM2"}]})

        assert api.client().cert.findings.get_all() == [{"id": "CM1"}, {"id": "CM2"}]

    def test_dismiss_and_restore(self, api: ApiServer) -> None:
        client = api.client()
        client.cert.findings.dismiss({"finding_id": ["CERT_CAA01", "CERT_CAA02"], "monitors": ["CM1", "CM2"]})
        client.cert.findings.restore({"finding_id": "CERT_CAA01"})

        assert api.requests[0]["path"] == "/4.0/cert/findings/dismiss.json"
        assert api.requests[0]["body"] == {"finding_id": ["CERT_CAA01,CERT_CAA02"], "monitors": ["CM1,CM2"]}
        assert api.requests[1]["path"] == "/4.0/cert/findings/restore.json"
        assert api.requests[1]["body"] == {"finding_id": ["CERT_CAA01"]}

    def test_monitor_check(self, api: ApiServer) -> None:
        api.client().cert.monitors.check("CMx")

        assert api.requests[0]["method"] == "POST"
        assert api.requests[0]["path"] == "/4.0/cert/monitors/CMx/check.json"

    def test_errors_count(self, api: ApiServer) -> None:
        api.reply(200, {"Content-Type": "text/plain"}, "3\n")

        assert api.client().cert.errors.count() == 3
        assert api.requests[0]["path"] == "/4.0/cert/errors/count.json"
