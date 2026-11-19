#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""RBL sources endpoint."""

from typing import Any, Dict, Optional, Union
from ..request_handler import RequestHandler
from ..pagination import PaginationMixin
from ...response import Response


class Sources(PaginationMixin):
    """Manage RBL sources."""

    def __init__(self, handler: RequestHandler) -> None:
        """Initialize the Sources endpoint.

        Args:
            handler: The request handler instance
        """
        self.handler = handler

    def get(
        self,
        id_or_params: Optional[Union[str, Dict[str, Any]]] = None,
        **options: Any
    ) -> Response:
        """Get sources or a single source.

        Args:
            id_or_params: Either a source ID string to get a single source,
                         or a dict of parameters to list sources
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with source data
        """
        if isinstance(id_or_params, str):
            # Get single source
            return self.handler.get(f"rbl/sources/{id_or_params}", **options)
        else:
            # List sources
            return self.handler.get("rbl/sources", id_or_params or {}, **options)

    def create(self, params: Dict[str, Any], **options: Any) -> Response:
        """Create a new RBL source.

        Args:
            params: Source creation parameters (name, host)
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with created source data
        """
        return self.handler.post("rbl/sources", params, idempotent=True, **options)

    def update(self, source_id: str, params: Dict[str, Any], **options: Any) -> Response:
        """Update an existing source.

        Args:
            source_id: The source ID to update
            params: Source parameters to update
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.put(f"rbl/sources/{source_id}", params, **options)

    def delete(self, source_id: str, **options: Any) -> Response:
        """Delete a source.

        Args:
            source_id: The source ID to delete
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.delete(f"rbl/sources/{source_id}", **options)

    def pause(self, source_id: str, **options: Any) -> Response:
        """Pause a source.

        Args:
            source_id: The source ID to pause
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.post(f"rbl/sources/{source_id}/pause", **options)

    def resume(self, source_id: str, **options: Any) -> Response:
        """Resume a source.

        Args:
            source_id: The source ID to resume
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.post(f"rbl/sources/{source_id}/resume", **options)

    def _get_resource_name(self) -> str:
        """Get the resource name for pagination."""
        return 'sources'
