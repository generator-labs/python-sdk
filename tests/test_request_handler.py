#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Tests for request handler array parameter conversion."""

import pytest
from unittest.mock import MagicMock, patch
from generatorlabs.api.request_handler import RequestHandler
from generatorlabs.exception import Exception as GLException


class TestArrayParameterConversion:
    """Test that array parameters are converted to comma-separated strings."""

    def _make_handler(self) -> RequestHandler:
        return RequestHandler(
            "AC" + "a" * 32,
            "b" * 64,
            "https://api.example.com/4.0/",
        )

    def test_list_converted_to_comma_separated_in_post(self) -> None:
        """Test that list values are joined with commas in POST requests."""
        handler = self._make_handler()
        captured_data: dict = {}

        def mock_post(url: str, data: dict = None, timeout: tuple = None):  # type: ignore[assignment]
            captured_data.update(data or {})
            response = MagicMock()
            response.json.return_value = {"status_code": 200, "status_message": "OK"}
            response.raise_for_status = MagicMock()
            return response

        handler.session.post = MagicMock(side_effect=mock_post)

        handler.post("rbl/hosts", {
            "name": "Test Host",
            "host": "1.2.3.4",
            "contact_group": [
                "CG11111111111111111111111111111111",
                "CG22222222222222222222222222222222",
            ],
        })

        assert captured_data["contact_group"] == (
            "CG11111111111111111111111111111111,CG22222222222222222222222222222222"
        )
        assert captured_data["name"] == "Test Host"

    def test_list_converted_to_comma_separated_in_put(self) -> None:
        """Test that list values are joined with commas in PUT requests."""
        handler = self._make_handler()
        captured_data: dict = {}

        def mock_put(url: str, data: dict = None, timeout: tuple = None):  # type: ignore[assignment]
            captured_data.update(data or {})
            response = MagicMock()
            response.json.return_value = {"status_code": 200, "status_message": "OK"}
            response.raise_for_status = MagicMock()
            return response

        handler.session.put = MagicMock(side_effect=mock_put)

        handler.put("rbl/hosts/HT11111111111111111111111111111111", {
            "contact_group": [
                "CG11111111111111111111111111111111",
                "CG22222222222222222222222222222222",
            ],
        })

        assert captured_data["contact_group"] == (
            "CG11111111111111111111111111111111,CG22222222222222222222222222222222"
        )

    def test_string_value_unchanged(self) -> None:
        """Test that string values are passed through unchanged."""
        handler = self._make_handler()
        captured_data: dict = {}

        def mock_post(url: str, data: dict = None, timeout: tuple = None):  # type: ignore[assignment]
            captured_data.update(data or {})
            response = MagicMock()
            response.json.return_value = {"status_code": 200, "status_message": "OK"}
            response.raise_for_status = MagicMock()
            return response

        handler.session.post = MagicMock(side_effect=mock_post)

        handler.post("rbl/hosts", {
            "name": "Test Host",
            "contact_group": "CG11111111111111111111111111111111",
        })

        assert captured_data["contact_group"] == "CG11111111111111111111111111111111"


class TestErrorResponses:
    """Test that 4xx/5xx responses raise with the API status_message and status_code."""

    def _make_handler(self) -> RequestHandler:
        return RequestHandler(
            "AC" + "a" * 32,
            "b" * 64,
            "https://api.example.com/4.0/",
        )

    def _response(self, status_code: int, body: dict) -> MagicMock:
        response = MagicMock()
        response.status_code = status_code
        response.json.return_value = body
        response.headers = {}
        return response

    def test_400_raises_with_status_message(self) -> None:
        handler = self._make_handler()
        handler.session.get = MagicMock(return_value=self._response(
            400, {"status_code": 400, "status_message": "Invalid host id provided."}))

        with pytest.raises(GLException) as exc:
            handler.get("rbl/hosts/HT11111111111111111111111111111111")

        assert "Invalid host id provided." in str(exc.value)
        assert exc.value.status_code == 400

    def test_404_raises(self) -> None:
        handler = self._make_handler()
        handler.session.get = MagicMock(return_value=self._response(
            404, {"status_code": 404, "status_message": "Not found."}))

        with pytest.raises(GLException) as exc:
            handler.get("rbl/hosts/HT11111111111111111111111111111111")

        assert exc.value.status_code == 404

    def test_422_raises_with_status_message(self) -> None:
        handler = self._make_handler()
        handler.session.post = MagicMock(return_value=self._response(
            422, {"status_code": 422, "status_message": "Validation failed."}))

        with pytest.raises(GLException) as exc:
            handler.post("rbl/hosts", {})

        assert "Validation failed." in str(exc.value)
        assert exc.value.status_code == 422

    def test_500_raises(self) -> None:
        handler = self._make_handler()
        handler.session.get = MagicMock(return_value=self._response(
            500, {"status_code": 500, "status_message": "Server error."}))

        with pytest.raises(GLException) as exc:
            handler.get("rbl/listings")

        assert exc.value.status_code == 500

    def test_200_does_not_raise(self) -> None:
        handler = self._make_handler()
        handler.session.get = MagicMock(return_value=self._response(
            200, {"status_code": 200, "status_message": "OK", "data": []}))

        result = handler.get("rbl/hosts")

        assert result is not None
