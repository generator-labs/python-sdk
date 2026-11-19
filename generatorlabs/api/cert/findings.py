#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Certificate findings endpoint."""

from typing import Any, Dict, Optional
from ..request_handler import RequestHandler
from ..pagination import PaginationMixin
from ...response import Response


class Findings(PaginationMixin):
    """List, dismiss and restore certificate findings."""

    def __init__(self, handler: RequestHandler) -> None:
        """Initialize the Findings endpoint.

        Args:
            handler: The request handler instance
        """
        self.handler = handler

    def get(self, params: Optional[Dict[str, Any]] = None, **options: Any) -> Response:
        """Get the current findings on the active certificate monitors.

        Args:
            params: Optional query parameters (page, page_size, dismissed)
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with one entry per monitor, each with its findings
        """
        return self.handler.get("cert/findings", params or {}, **options)

    def dismiss(self, params: Dict[str, Any], **options: Any) -> Response:
        """Dismiss findings.

        Args:
            params: The findings to dismiss (finding_id, monitors); leave monitors out
                    to dismiss from every active monitor that has the finding
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with the monitors changed
        """
        return self.handler.post("cert/findings/dismiss", params, **options)

    def restore(self, params: Dict[str, Any], **options: Any) -> Response:
        """Restore dismissed findings.

        Args:
            params: The findings to restore (finding_id, monitors); leave monitors out
                    to restore on every monitor the finding is dismissed from
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with the monitors changed
        """
        return self.handler.post("cert/findings/restore", params, **options)

    def _get_resource_name(self) -> str:
        """Get the resource name for pagination."""
        return 'data'
