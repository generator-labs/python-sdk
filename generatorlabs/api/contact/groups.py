#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Contact groups endpoint."""

from typing import Any, Dict, Optional, Union
from ..request_handler import RequestHandler
from ..pagination import PaginationMixin


class Groups(PaginationMixin):
    """Manage contact groups."""

    def __init__(self, handler: RequestHandler) -> None:
        """Initialize the Groups endpoint.

        Args:
            handler: The request handler instance
        """
        self.handler = handler

    def get(
        self,
        id_or_params: Optional[Union[str, Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Get groups or a single group.

        Args:
            id_or_params: Either a group ID string to get a single group,
                         or a dict of parameters to list groups

        Returns:
            API response with group data
        """
        if isinstance(id_or_params, str):
            # Get single group
            return self.handler.get(f"contact/groups/{id_or_params}")
        else:
            # List groups
            return self.handler.get("contact/groups", id_or_params or {})

    def create(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new contact group.

        Args:
            params: Group creation parameters (name, contacts)

        Returns:
            API response with created group data
        """
        return self.handler.post("contact/groups", params)

    def update(self, group_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing group.

        Args:
            group_id: The group ID to update
            params: Group parameters to update

        Returns:
            API response
        """
        return self.handler.put(f"contact/groups/{group_id}", params)

    def delete(self, group_id: str) -> Dict[str, Any]:
        """Delete a group.

        Args:
            group_id: The group ID to delete

        Returns:
            API response
        """
        return self.handler.delete(f"contact/groups/{group_id}")

    def _get_resource_name(self) -> str:
        """Get the resource name for pagination."""
        return 'groups'
