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
from ..config import Config
from ..response import Response as ApiResponse, RateLimitInfo

if TYPE_CHECKING:
    from ..client import Client


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
        retry_strategy = Retry(
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

    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None
    ) -> ApiResponse:
        """Make an HTTP request to the API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API endpoint path
            params: Request parameters

        Returns:
            API response wrapper with data and rate limit info

        Raises:
            Exception: If the request fails or response is invalid
        """
        url = f"{self.api_url}{path}.json"

        # Timeouts: (connect_timeout, read_timeout)
        timeout = (self.config.connect_timeout, self.config.timeout)

        # Convert list values to comma-separated strings for form encoding
        if params:
            for key, value in params.items():
                if isinstance(value, list):
                    params[key] = ",".join(str(v) for v in value)

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

        # Parse rate limit headers
        rate_limit_info = None
        if 'RateLimit-Limit' in response.headers:
            rate_limit_info = RateLimitInfo(
                limit=response.headers['RateLimit-Limit'],
                remaining=int(response.headers.get('RateLimit-Remaining', '0')),
                reset=int(response.headers.get('RateLimit-Reset', '0'))
            )

        return ApiResponse(json_data, rate_limit_info)

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> ApiResponse:
        """Make a GET request."""
        return self._make_request("GET", path, params)

    def post(self, path: str, params: Optional[Dict[str, Any]] = None) -> ApiResponse:
        """Make a POST request."""
        return self._make_request("POST", path, params)

    def put(self, path: str, params: Optional[Dict[str, Any]] = None) -> ApiResponse:
        """Make a PUT request."""
        return self._make_request("PUT", path, params)

    def delete(self, path: str) -> ApiResponse:
        """Make a DELETE request."""
        return self._make_request("DELETE", path)
