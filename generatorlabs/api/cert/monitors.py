#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Certificate monitors endpoint."""

from typing import Any, Dict, Optional, Union
from ..request_handler import RequestHandler
from ..pagination import PaginationMixin
from ...response import Response


class Monitors(PaginationMixin):
    """Manage certificate monitors."""

    def __init__(self, handler: RequestHandler) -> None:
        """Initialize the Monitors endpoint.

        Args:
            handler: The request handler instance
        """
        self.handler = handler

    def get(
        self,
        id_or_params: Optional[Union[str, Dict[str, Any]]] = None,
        **options: Any
    ) -> Response:
        """Get monitors or a single monitor.

        Args:
            id_or_params: Either a monitor ID string to get a single monitor,
                         or a dict of parameters to list monitors
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with monitor data
        """
        if isinstance(id_or_params, str):
            # Get single monitor
            return self.handler.get(f"cert/monitors/{id_or_params}", **options)
        else:
            # List monitors
            return self.handler.get("cert/monitors", id_or_params or {}, **options)

    def create(self, params: Dict[str, Any], **options: Any) -> Response:
        """Create a new certificate monitor.

        Args:
            params: Monitor creation parameters (hostname, protocol, name, profile, contact_group)
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with created monitor data
        """
        return self.handler.post("cert/monitors", params, idempotent=True, **options)

    def update(self, monitor_id: str, params: Dict[str, Any], **options: Any) -> Response:
        """Update an existing monitor.

        Args:
            monitor_id: The monitor ID to update
            params: Monitor parameters to update
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.put(f"cert/monitors/{monitor_id}", params, **options)

    def delete(self, monitor_id: str, **options: Any) -> Response:
        """Delete a monitor.

        Args:
            monitor_id: The monitor ID to delete
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.delete(f"cert/monitors/{monitor_id}", idempotent=True, **options)

    def pause(self, monitor_id: str, **options: Any) -> Response:
        """Pause monitoring for a certificate.

        Args:
            monitor_id: The monitor ID to pause
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.post(f"cert/monitors/{monitor_id}/pause", **options)

    def resume(self, monitor_id: str, **options: Any) -> Response:
        """Resume monitoring for a certificate.

        Args:
            monitor_id: The monitor ID to resume
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.post(f"cert/monitors/{monitor_id}/resume", **options)

    def check(self, monitor_id: str, **options: Any) -> Response:
        """Queue a check of a certificate monitor now.

        Args:
            monitor_id: The monitor ID to check
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with the queued check
        """
        return self.handler.post(f"cert/monitors/{monitor_id}/check", idempotent=True, **options)

    def _get_resource_name(self) -> str:
        """Get the resource name for pagination."""
        return 'monitors'
