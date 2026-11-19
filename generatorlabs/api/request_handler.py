#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""HTTP request handler for the Generator Labs API."""

from typing import Any, Dict, Optional, TYPE_CHECKING
import uuid
import requests
from requests.adapters import HTTPAdapter
from urllib3.exceptions import MaxRetryError, ResponseError
from urllib3.util.retry import Retry
from ..exception import Exception
from ..config import Config
from ..response import Response as ApiResponse, RateLimitInfo

if TYPE_CHECKING:
    from ..client import Client


# The longest Retry-After (in seconds) that is waited out before a retry. A longer wait is not
# slept: the response is returned as the error instead.
MAX_RETRY_AFTER = 60

# The options any request accepts
REQUEST_OPTIONS = ("idempotency_key", "request_id", "if_none_match", "fields")


class CappedRetry(Retry):
    """Retry strategy that gives up when the Retry-After header asks for a long wait."""

    def increment(
        self,
        method: Any = None,
        url: Any = None,
        response: Any = None,
        error: Any = None,
        _pool: Any = None,
        _stacktrace: Any = None
    ) -> Any:
        """Stop retrying when the response asks to wait longer than MAX_RETRY_AFTER."""
        if response is not None:
            retry_after = self.get_retry_after(response)
            if retry_after is not None and retry_after > MAX_RETRY_AFTER:
                raise MaxRetryError(
                    _pool, url, ResponseError(f"Retry-After of {retry_after} seconds is too long")
                )

        return super().increment(method, url, response, error, _pool, _stacktrace)


class RequestHandler:
    """Handles HTTP requests to the Generator Labs API."""

    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        api_url: str,
        config: Optional[Config] = None
    ) -> None:
        """Initialize the request handler.

        Args:
            account_sid: The account SID for authentication
            auth_token: The auth token for authentication
            api_url: The base API URL
            config: Configuration object
        """
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.api_url = api_url
        self.auth = (account_sid, auth_token)
        self.config = config or Config()

        # Initialize session with retry logic and timeouts
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic and configuration.

        Returns:
            Configured requests.Session with retry adapter
        """
        # Import VERSION here to avoid circular import
        from ..client import Client

        session = requests.Session()

        # Configure retry strategy with exponential backoff
        retry_strategy = CappedRetry(
            total=self.config.max_retries,  # Maximum number of retries
            backoff_factor=self.config.retry_backoff,  # Exponential backoff multiplier
            status_forcelist=[429, 500, 502, 503, 504],  # HTTP status codes to retry
            allowed_methods=["GET", "POST", "PUT", "DELETE"],  # Methods to retry
            raise_on_status=False,  # Don't raise on retry exhaustion
            respect_retry_after_header=True,  # Use Retry-After header from rate limit responses
        )

        # Mount adapter with retry strategy
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set default headers
        session.headers.update({
            "User-Agent": f"GeneratorLabs-Python/{Client.VERSION}",
            "Accept": "application/json",
        })

        # Set authentication
        session.auth = self.auth

        return session

    def _send(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]],
        options: Dict[str, Any],
        idempotent: bool = False
    ) -> requests.Response:
        """Send an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            params: Request parameters
            options: Request options (idempotency_key, request_id, if_none_match, fields)
            idempotent: Whether the endpoint accepts an Idempotency-Key; one is generated
                        when the caller gave none

        Returns:
            The HTTP response

        Raises:
            Exception: If an option is unknown or the request fails
        """
        url = f"{self.api_url}{path}.json"

        # Timeouts: (connect_timeout, read_timeout)
        timeout = (self.config.connect_timeout, self.config.timeout)

        unknown = sorted(set(options) - set(REQUEST_OPTIONS))
        if unknown:
            raise Exception(f"Unknown request option: {', '.join(unknown)}")

        # The headers are set once per call, so every retry of the call sends the same
        # Idempotency-Key and the API answers a repeat with the first result
        headers: Dict[str, str] = {}
        if options.get("idempotency_key") is not None:
            headers["Idempotency-Key"] = str(options["idempotency_key"])
        elif idempotent:
            headers["Idempotency-Key"] = str(uuid.uuid4())
        if options.get("request_id") is not None:
            headers["X-Request-Id"] = str(options["request_id"])
        if options.get("if_none_match") is not None:
            headers["If-None-Match"] = str(options["if_none_match"])

        # Field selection applies to GET requests
        if method == "GET" and options.get("fields") is not None:
            params = {**(params or {}), "fields": options["fields"]}

        # Convert list values to comma-separated strings for form encoding
        if params:
            for key, value in params.items():
                if isinstance(value, list):
                    params[key] = ",".join(str(v) for v in value)

        try:
            if method == "GET":
                return self.session.get(url, params=params, headers=headers, timeout=timeout)
            elif method == "POST":
                return self.session.post(url, data=params, headers=headers, timeout=timeout)
            elif method == "PUT":
                return self.session.put(url, data=params, headers=headers, timeout=timeout)
            elif method == "DELETE":
                return self.session.delete(url, headers=headers, timeout=timeout)
            else:
                raise Exception(f"Unsupported HTTP method: {method}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        options: Optional[Dict[str, Any]] = None,
        idempotent: bool = False
    ) -> ApiResponse:
        """Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            params: Request parameters
            options: Request options (idempotency_key, request_id, if_none_match, fields)
            idempotent: Whether the endpoint accepts an Idempotency-Key

        Returns:
            API response wrapper with data, rate limit info and response metadata

        Raises:
            Exception: If the request fails or response is invalid
        """
        response = self._send(method, path, params, options or {}, idempotent)
        request_id = response.headers.get("X-Request-Id")

        # Parse rate limit headers
        rate_limit_info = None
        if 'RateLimit-Limit' in response.headers:
            rate_limit_info = RateLimitInfo(
                limit=response.headers['RateLimit-Limit'],
                remaining=int(response.headers.get('RateLimit-Remaining', '0')),
                reset=int(response.headers.get('RateLimit-Reset', '0'))
            )

        # 304 Not Modified has no body: the copy the caller's ETag came from is still current
        if response.status_code == 304:
            return ApiResponse(
                {},
                rate_limit_info,
                request_id=request_id,
                etag=response.headers.get("ETag"),
                not_modified=True
            )

        # Parse the JSON body first so the API's status_message survives, then determine
        # success vs failure from status_code (which mirrors the HTTP status code).
        try:
            json_data: Dict[str, Any] = response.json()
        except ValueError:
            if response.status_code >= 400:
                raise Exception(
                    f"HTTP {response.status_code} error", response.status_code, request_id
                )
            raise Exception("Failed to parse JSON response", None, request_id)

        code = (
            json_data["status_code"]
            if isinstance(json_data, dict) and "status_code" in json_data
            else response.status_code
        )
        if code >= 400:
            message = (
                json_data.get("status_message") if isinstance(json_data, dict) else None
            ) or f"HTTP {response.status_code} error"
            raise Exception(f"API error: {message}", code, request_id)

        return ApiResponse(
            json_data,
            rate_limit_info,
            request_id=request_id,
            etag=response.headers.get("ETag"),
            replayed=response.headers.get("Idempotent-Replayed") == "true"
        )

    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        **options: Any
    ) -> ApiResponse:
        """Make a GET request."""
        return self._make_request("GET", path, params, options)

    def get_plain(self, path: str, **options: Any) -> str:
        """Make a GET request to an endpoint that answers in plain text.

        Returns:
            The response body

        Raises:
            Exception: If the request fails or the HTTP status is 400 or greater
        """
        response = self._send("GET", path, None, options)

        if response.status_code >= 400:
            raise Exception(
                f"HTTP {response.status_code} error",
                response.status_code,
                response.headers.get("X-Request-Id")
            )

        return response.text.strip()

    def post(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        idempotent: bool = False,
        **options: Any
    ) -> ApiResponse:
        """Make a POST request."""
        return self._make_request("POST", path, params, options, idempotent)

    def put(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        **options: Any
    ) -> ApiResponse:
        """Make a PUT request."""
        return self._make_request("PUT", path, params, options)

    def delete(self, path: str, idempotent: bool = False, **options: Any) -> ApiResponse:
        """Make a DELETE request."""
        return self._make_request("DELETE", path, None, options, idempotent)
