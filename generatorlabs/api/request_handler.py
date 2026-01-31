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
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from ..exception import Exception

if TYPE_CHECKING:
    from ..client import Client


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
        # Retries: 0, 1, 2 (3 total attempts)
        # Backoff delays: 1s, 2s, 4s
        retry_strategy = Retry(
            total=3,  # Maximum number of retries
            backoff_factor=1,  # Exponential backoff: 1 * (2 ** retry_number)
            status_forcelist=[429, 500, 502, 503, 504],  # HTTP status codes to retry
            allowed_methods=["GET", "POST", "PUT", "DELETE"],  # Methods to retry
            raise_on_status=False,  # Don't raise on retry exhaustion
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

        # Timeouts: (connect_timeout, read_timeout)
        timeout = (5.0, 30.0)

        try:
            if method == "GET":
                response = self.session.get(url, params=params, timeout=timeout)
            elif method == "POST":
                response = self.session.post(url, data=params, timeout=timeout)
            elif method == "PUT":
                response = self.session.put(url, data=params, timeout=timeout)
            elif method == "DELETE":
                response = self.session.delete(url, timeout=timeout)
            else:
                raise Exception(f"Unsupported HTTP method: {method}")

            # Check HTTP status code
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
