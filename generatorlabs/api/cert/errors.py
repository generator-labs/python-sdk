#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Certificate errors endpoint."""

from typing import Any, Dict, Optional
from ..request_handler import RequestHandler
from ..pagination import PaginationMixin


class Errors(PaginationMixin):
    """Get current certificate errors."""

    def __init__(self, handler: RequestHandler) -> None:
        """Initialize the Errors endpoint.

        Args:
            handler: The request handler instance
        """
        self.handler = handler

    def get(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Get current certificate errors.

        Args:
            params: Optional query parameters (page, page_size, search, sort)

        Returns:
            API response with error data
        """
        return self.handler.get("cert/errors", params or {})

    def _get_resource_name(self) -> str:
        """Get the resource name for pagination."""
        return 'errors'
