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
        id_or_params: Optional[Union[str, Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Get sources or a single source.

        Args:
            id_or_params: Either a source ID string to get a single source,
                         or a dict of parameters to list sources

        Returns:
            API response with source data
        """
        if isinstance(id_or_params, str):
            # Get single source
            return self.handler.get(f"rbl/sources/{id_or_params}")
        else:
            # List sources
            return self.handler.get("rbl/sources", id_or_params or {})

    def create(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new RBL source.

        Args:
            params: Source creation parameters (name, host)

        Returns:
            API response with created source data
        """
        return self.handler.post("rbl/sources", params)

    def update(self, source_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing source.

        Args:
            source_id: The source ID to update
            params: Source parameters to update

        Returns:
            API response
        """
        return self.handler.put(f"rbl/sources/{source_id}", params)

    def delete(self, source_id: str) -> Dict[str, Any]:
        """Delete a source.

        Args:
            source_id: The source ID to delete

        Returns:
            API response
        """
        return self.handler.delete(f"rbl/sources/{source_id}")

    def pause(self, source_id: str) -> Dict[str, Any]:
        """Pause a source.

        Args:
            source_id: The source ID to pause

        Returns:
            API response
        """
        return self.handler.post(f"rbl/sources/{source_id}/pause")

    def resume(self, source_id: str) -> Dict[str, Any]:
        """Resume a source.

        Args:
            source_id: The source ID to resume

        Returns:
            API response
        """
        return self.handler.post(f"rbl/sources/{source_id}/resume")

    def _get_resource_name(self) -> str:
        """Get the resource name for pagination."""
        return 'sources'
