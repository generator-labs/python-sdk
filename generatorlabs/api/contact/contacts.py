#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Contacts endpoint."""

from typing import Any, Dict, Optional, Union
from ..request_handler import RequestHandler
from ..pagination import PaginationMixin
from ...response import Response


class Contacts(PaginationMixin):
    """Manage notification contacts."""

    def __init__(self, handler: RequestHandler) -> None:
        """Initialize the Contacts endpoint.

        Args:
            handler: The request handler instance
        """
        self.handler = handler

    def get(
        self,
        id_or_params: Optional[Union[str, Dict[str, Any]]] = None,
        **options: Any
    ) -> Response:
        """Get contacts or a single contact.

        Args:
            id_or_params: Either a contact ID string to get a single contact,
                         or a dict of parameters to list contacts
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with contact data
        """
        if isinstance(id_or_params, str):
            # Get single contact
            return self.handler.get(f"contact/contacts/{id_or_params}", **options)
        else:
            # List contacts
            return self.handler.get("contact/contacts", id_or_params or {}, **options)

    def create(self, params: Dict[str, Any], **options: Any) -> Response:
        """Create a new contact.

        Args:
            params: Contact creation parameters (email, type)
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with created contact data
        """
        return self.handler.post("contact/contacts", params, idempotent=True, **options)

    def update(self, contact_id: str, params: Dict[str, Any], **options: Any) -> Response:
        """Update an existing contact.

        Args:
            contact_id: The contact ID to update
            params: Contact parameters to update
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.put(f"contact/contacts/{contact_id}", params, **options)

    def delete(self, contact_id: str, **options: Any) -> Response:
        """Delete a contact.

        Args:
            contact_id: The contact ID to delete
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.delete(f"contact/contacts/{contact_id}", **options)

    def pause(self, contact_id: str, **options: Any) -> Response:
        """Pause a contact.

        Args:
            contact_id: The contact ID to pause
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.post(f"contact/contacts/{contact_id}/pause", **options)

    def resume(self, contact_id: str, **options: Any) -> Response:
        """Resume a contact.

        Args:
            contact_id: The contact ID to resume
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.post(f"contact/contacts/{contact_id}/resume", **options)

    def confirm(self, contact_id: str, params: Dict[str, Any], **options: Any) -> Response:
        """Confirm a contact with an auth code.

        Args:
            contact_id: The contact ID to confirm
            params: Confirmation parameters (authcode)
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.post(f"contact/contacts/{contact_id}/confirm", params, idempotent=True, **options)

    def resend(self, contact_id: str, **options: Any) -> Response:
        """Resend confirmation to a contact.

        Args:
            contact_id: The contact ID
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.post(f"contact/contacts/{contact_id}/resend", idempotent=True, **options)

    def _get_resource_name(self) -> str:
        """Get the resource name for pagination."""
        return 'contacts'
