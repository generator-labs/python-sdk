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


class Contacts:
    """Manage notification contacts."""

    def __init__(self, handler: RequestHandler) -> None:
        """Initialize the Contacts endpoint.

        Args:
            handler: The request handler instance
        """
        self.handler = handler

    def get(
        self,
        id_or_params: Optional[Union[str, Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Get contacts or a single contact.

        Args:
            id_or_params: Either a contact ID string to get a single contact,
                         or a dict of parameters to list contacts

        Returns:
            API response with contact data
        """
        if isinstance(id_or_params, str):
            # Get single contact
            return self.handler.get(f"contact/contacts/{id_or_params}")
        else:
            # List contacts
            return self.handler.get("contact/contacts", id_or_params or {})

    def create(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new contact.

        Args:
            params: Contact creation parameters (email, type)

        Returns:
            API response with created contact data
        """
        return self.handler.post("contact/contacts", params)

    def update(self, contact_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing contact.

        Args:
            contact_id: The contact ID to update
            params: Contact parameters to update

        Returns:
            API response
        """
        return self.handler.put(f"contact/contacts/{contact_id}", params)

    def delete(self, contact_id: str) -> Dict[str, Any]:
        """Delete a contact.

        Args:
            contact_id: The contact ID to delete

        Returns:
            API response
        """
        return self.handler.delete(f"contact/contacts/{contact_id}")

    def pause(self, contact_id: str) -> Dict[str, Any]:
        """Pause a contact.

        Args:
            contact_id: The contact ID to pause

        Returns:
            API response
        """
        return self.handler.post(f"contact/contacts/{contact_id}/pause")

    def resume(self, contact_id: str) -> Dict[str, Any]:
        """Resume a contact.

        Args:
            contact_id: The contact ID to resume

        Returns:
            API response
        """
        return self.handler.post(f"contact/contacts/{contact_id}/resume")

    def confirm(self, contact_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Confirm a contact with an auth code.

        Args:
            contact_id: The contact ID to confirm
            params: Confirmation parameters (authcode)

        Returns:
            API response
        """
        return self.handler.post(f"contact/contacts/{contact_id}/confirm", params)

    def resend(self, contact_id: str) -> Dict[str, Any]:
        """Resend confirmation to a contact.

        Args:
            contact_id: The contact ID

        Returns:
            API response
        """
        return self.handler.post(f"contact/contacts/{contact_id}/resend")
