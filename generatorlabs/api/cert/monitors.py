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
        id_or_params: Optional[Union[str, Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Get monitors or a single monitor.

        Args:
            id_or_params: Either a monitor ID string to get a single monitor,
                         or a dict of parameters to list monitors

        Returns:
            API response with monitor data
        """
        if isinstance(id_or_params, str):
            # Get single monitor
            return self.handler.get(f"cert/monitors/{id_or_params}")
        else:
            # List monitors
            return self.handler.get("cert/monitors", id_or_params or {})

    def create(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new certificate monitor.

        Args:
            params: Monitor creation parameters (name, host, type, cert_profile, contact_group)

        Returns:
            API response with created monitor data
        """
        return self.handler.post("cert/monitors", params)

    def update(self, monitor_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing monitor.

        Args:
            monitor_id: The monitor ID to update
            params: Monitor parameters to update

        Returns:
            API response
        """
        return self.handler.put(f"cert/monitors/{monitor_id}", params)

    def delete(self, monitor_id: str) -> Dict[str, Any]:
        """Delete a monitor.

        Args:
            monitor_id: The monitor ID to delete

        Returns:
            API response
        """
        return self.handler.delete(f"cert/monitors/{monitor_id}")

    def pause(self, monitor_id: str) -> Dict[str, Any]:
        """Pause monitoring for a certificate.

        Args:
            monitor_id: The monitor ID to pause

        Returns:
            API response
        """
        return self.handler.post(f"cert/monitors/{monitor_id}/pause")

    def resume(self, monitor_id: str) -> Dict[str, Any]:
        """Resume monitoring for a certificate.

        Args:
            monitor_id: The monitor ID to resume

        Returns:
            API response
        """
        return self.handler.post(f"cert/monitors/{monitor_id}/resume")

    def _get_resource_name(self) -> str:
        """Get the resource name for pagination."""
        return 'monitors'
