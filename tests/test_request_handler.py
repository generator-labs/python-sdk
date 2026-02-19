#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Tests for request handler array parameter conversion."""

from unittest.mock import MagicMock, patch
from generatorlabs.api.request_handler import RequestHandler


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
