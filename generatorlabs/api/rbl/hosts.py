#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Hosts endpoint for RBL monitoring."""

from typing import Any, Dict, Optional, Union
from ..request_handler import RequestHandler
from ..pagination import PaginationMixin
from ...response import Response


class Hosts(PaginationMixin):
    """Manage RBL monitored hosts."""

    def __init__(self, handler: RequestHandler) -> None:
        """Initialize the Hosts endpoint.

        Args:
            handler: The request handler instance
        """
        self.handler = handler

    def get(
        self,
        id_or_params: Optional[Union[str, Dict[str, Any]]] = None,
        **options: Any
    ) -> Response:
        """Get hosts or a single host.

        Args:
            id_or_params: Either a host ID string to get a single host,
                         or a dict of parameters to list hosts
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with host data
        """
        if isinstance(id_or_params, str):
            # Get single host
            return self.handler.get(f"rbl/hosts/{id_or_params}", **options)
        else:
            # List hosts
            return self.handler.get("rbl/hosts", id_or_params or {}, **options)

    def create(self, params: Dict[str, Any], **options: Any) -> Response:
        """Create a new monitored host.

        Args:
            params: Host creation parameters (name, host, profile, contact_group)
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with created host data
        """
        return self.handler.post("rbl/hosts", params, idempotent=True, **options)

    def update(self, host_id: str, params: Dict[str, Any], **options: Any) -> Response:
        """Update an existing host.

        Args:
            host_id: The host ID to update
            params: Host parameters to update
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.put(f"rbl/hosts/{host_id}", params, **options)

    def delete(self, host_id: str, **options: Any) -> Response:
        """Delete a host.

        Args:
            host_id: The host ID to delete
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.delete(f"rbl/hosts/{host_id}", **options)

    def pause(self, host_id: str, **options: Any) -> Response:
        """Pause monitoring for a host.

        Args:
            host_id: The host ID to pause
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.post(f"rbl/hosts/{host_id}/pause", **options)

    def resume(self, host_id: str, **options: Any) -> Response:
        """Resume monitoring for a host.

        Args:
            host_id: The host ID to resume
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.post(f"rbl/hosts/{host_id}/resume", **options)

    def _get_resource_name(self) -> str:
        """Get the resource name for pagination."""
        return 'hosts'
