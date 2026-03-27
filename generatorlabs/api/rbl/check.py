#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Manual RBL check endpoint."""

from typing import Any, Dict, Optional
from ..request_handler import RequestHandler
from ...response import Response


class Check:
    """Perform manual RBL checks."""

    def __init__(self, handler: RequestHandler) -> None:
        """Initialize the Check endpoint.

        Args:
            handler: The request handler instance
        """
        self.handler = handler

    def start(self, params: Dict[str, Any]) -> Response:
        """Start a manual RBL check.

        Args:
            params: Check parameters (host, callback, details)

        Returns:
            API response with check ID
        """
        return self.handler.post("rbl/check/start", params)

    def status(
        self,
        check_id: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Response:
        """Get the status of a manual check.

        Args:
            check_id: The check ID
            params: Optional parameters (details)

        Returns:
            API response with check status
        """
        return self.handler.get(f"rbl/check/status/{check_id}", params or {})
