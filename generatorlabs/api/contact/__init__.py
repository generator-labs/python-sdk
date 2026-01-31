#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Contact management API endpoints."""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..request_handler import RequestHandler

from .contacts import Contacts
from .groups import Groups


class Contact:
    """Contact management namespace."""

    def __init__(self, handler: "RequestHandler") -> None:
        """Initialize the Contact namespace.

        Args:
            handler: The request handler instance
        """
        self._handler = handler
        self._contacts: Optional[Contacts] = None
        self._groups: Optional[Groups] = None

    @property
    def contacts(self) -> Contacts:
        """Get the Contacts endpoint."""
        if self._contacts is None:
            self._contacts = Contacts(self._handler)
        return self._contacts

    @property
    def groups(self) -> Groups:
        """Get the Groups endpoint."""
        if self._groups is None:
            self._groups = Groups(self._handler)
        return self._groups


__all__ = ["Contact", "Contacts", "Groups"]
