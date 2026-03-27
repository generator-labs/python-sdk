#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""RBL monitoring profiles endpoint."""

from typing import Any, Dict, Optional, Union
from ..request_handler import RequestHandler
from ..pagination import PaginationMixin
from ...response import Response


class Profiles(PaginationMixin):
    """Manage RBL monitoring profiles."""

    def __init__(self, handler: RequestHandler) -> None:
        """Initialize the Profiles endpoint.

        Args:
            handler: The request handler instance
        """
        self.handler = handler

    def get(
        self,
        id_or_params: Optional[Union[str, Dict[str, Any]]] = None
    ) -> Response:
        """Get profiles or a single profile.

        Args:
            id_or_params: Either a profile ID string to get a single profile,
                         or a dict of parameters to list profiles

        Returns:
            API response with profile data
        """
        if isinstance(id_or_params, str):
            # Get single profile
            return self.handler.get(f"rbl/profiles/{id_or_params}")
        else:
            # List profiles
            return self.handler.get("rbl/profiles", id_or_params or {})

    def create(self, params: Dict[str, Any]) -> Response:
        """Create a new monitoring profile.

        Args:
            params: Profile creation parameters (name, rbls)

        Returns:
            API response with created profile data
        """
        return self.handler.post("rbl/profiles", params)

    def update(self, profile_id: str, params: Dict[str, Any]) -> Response:
        """Update an existing profile.

        Args:
            profile_id: The profile ID to update
            params: Profile parameters to update

        Returns:
            API response
        """
        return self.handler.put(f"rbl/profiles/{profile_id}", params)

    def delete(self, profile_id: str) -> Response:
        """Delete a profile.

        Args:
            profile_id: The profile ID to delete

        Returns:
            API response
        """
        return self.handler.delete(f"rbl/profiles/{profile_id}")

    def _get_resource_name(self) -> str:
        """Get the resource name for pagination."""
        return 'profiles'
