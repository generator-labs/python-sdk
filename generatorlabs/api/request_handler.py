#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""HTTP request handler for the Generator Labs API."""

from typing import Any, Dict, Optional
import requests
from ..exception import Exception


class RequestHandler:
    """Handles HTTP requests to the Generator Labs API."""

    def __init__(self, account_sid: str, auth_token: str, api_url: str) -> None:
        """Initialize the request handler.

        Args:
            account_sid: The account SID for authentication
            auth_token: The auth token for authentication
            api_url: The base API URL
        """
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.api_url = api_url
        self.auth = (account_sid, auth_token)

    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            params: Request parameters

        Returns:
            JSON response as a dictionary

        Raises:
            Exception: If the request fails or response is invalid
        """
        url = f"{self.api_url}{path}.json"

        try:
            if method == "GET":
                response = requests.get(url, params=params, auth=self.auth)
            elif method == "POST":
                response = requests.post(url, data=params, auth=self.auth)
            elif method == "PUT":
                response = requests.put(url, data=params, auth=self.auth)
            elif method == "DELETE":
                response = requests.delete(url, auth=self.auth)
            else:
                raise Exception(f"Unsupported HTTP method: {method}")

            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

        try:
            json_data: Dict[str, Any] = response.json()
        except ValueError:
            raise Exception("Failed to parse JSON response")

        # Check v4.0 API response format
        if isinstance(json_data, dict) and json_data.get("success") is False:
            error_msg = json_data.get("error", {}).get("message", "Unknown error")
            raise Exception(f"API error: {error_msg}")

        return json_data

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request."""
        return self._make_request("GET", path, params)

    def post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a POST request."""
        return self._make_request("POST", path, params)

    def put(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a PUT request."""
        return self._make_request("PUT", path, params)

    def delete(self, path: str) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self._make_request("DELETE", path)
