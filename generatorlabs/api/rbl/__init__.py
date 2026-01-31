#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""RBL monitoring API endpoints."""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..request_handler import RequestHandler

from .hosts import Hosts
from .check import Check
from .listings import Listings
from .profiles import Profiles
from .sources import Sources


class RBL:
    """RBL monitoring namespace."""

    def __init__(self, handler: "RequestHandler") -> None:
        """Initialize the RBL namespace.

        Args:
            handler: The request handler instance
        """
        self._handler = handler
        self._hosts: Optional[Hosts] = None
        self._check: Optional[Check] = None
        self._listings: Optional[Listings] = None
        self._profiles: Optional[Profiles] = None
        self._sources: Optional[Sources] = None

    @property
    def hosts(self) -> Hosts:
        """Get the Hosts endpoint."""
        if self._hosts is None:
            self._hosts = Hosts(self._handler)
        return self._hosts

    @property
    def check(self) -> Check:
        """Get the Check endpoint."""
        if self._check is None:
            self._check = Check(self._handler)
        return self._check

    @property
    def listings(self) -> Listings:
        """Get the Listings endpoint."""
        if self._listings is None:
            self._listings = Listings(self._handler)
        return self._listings

    @property
    def profiles(self) -> Profiles:
        """Get the Profiles endpoint."""
        if self._profiles is None:
            self._profiles = Profiles(self._handler)
        return self._profiles

    @property
    def sources(self) -> Sources:
        """Get the Sources endpoint."""
        if self._sources is None:
            self._sources = Sources(self._handler)
        return self._sources


__all__ = ["RBL", "Hosts", "Check", "Listings", "Profiles", "Sources"]
