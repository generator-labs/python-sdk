#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Certificate profiles endpoint."""

from typing import Any, Dict, Optional, Union
from ..request_handler import RequestHandler
from ..pagination import PaginationMixin
from ...response import Response


class Profiles(PaginationMixin):
    """Manage certificate monitoring profiles."""

    def __init__(self, handler: RequestHandler) -> None:
        """Initialize the Profiles endpoint.

        Args:
            handler: The request handler instance
        """
        self.handler = handler

    def get(
        self,
        id_or_params: Optional[Union[str, Dict[str, Any]]] = None,
        **options: Any
    ) -> Response:
        """Get profiles or a single profile.

        Args:
            id_or_params: Either a profile ID string to get a single profile,
                         or a dict of parameters to list profiles
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with profile data
        """
        if isinstance(id_or_params, str):
            # Get single profile
            return self.handler.get(f"cert/profiles/{id_or_params}", **options)
        else:
            # List profiles
            return self.handler.get("cert/profiles", id_or_params or {}, **options)

    def create(self, params: Dict[str, Any], **options: Any) -> Response:
        """Create a new certificate monitoring profile.

        Args:
            params: Profile creation parameters (name, check_frequency, expiry_threshold, etc.)
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with created profile data
        """
        return self.handler.post("cert/profiles", params, idempotent=True, **options)

    def update(self, profile_id: str, params: Dict[str, Any], **options: Any) -> Response:
        """Update an existing profile.

        Args:
            profile_id: The profile ID to update
            params: Profile parameters to update
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.put(f"cert/profiles/{profile_id}", params, **options)

    def delete(self, profile_id: str, **options: Any) -> Response:
        """Delete a profile.

        Args:
            profile_id: The profile ID to delete
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.delete(f"cert/profiles/{profile_id}", **options)

    def _get_resource_name(self) -> str:
        """Get the resource name for pagination."""
        return 'profiles'
