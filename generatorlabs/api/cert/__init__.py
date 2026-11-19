#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Certificate monitoring API endpoints."""

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..request_handler import RequestHandler

from .errors import Errors
from .findings import Findings
from .monitors import Monitors
from .profiles import Profiles


class Cert:
    """Certificate monitoring namespace."""

    def __init__(self, handler: "RequestHandler") -> None:
        """Initialize the Cert namespace.

        Args:
            handler: The request handler instance
        """
        self._handler = handler
        self._errors: Optional[Errors] = None
        self._findings: Optional[Findings] = None
        self._monitors: Optional[Monitors] = None
        self._profiles: Optional[Profiles] = None

    @property
    def errors(self) -> Errors:
        """Get the Errors endpoint."""
        if self._errors is None:
            self._errors = Errors(self._handler)
        return self._errors

    @property
    def findings(self) -> Findings:
        """Get the Findings endpoint."""
        if self._findings is None:
            self._findings = Findings(self._handler)
        return self._findings

    @property
    def monitors(self) -> Monitors:
        """Get the Monitors endpoint."""
        if self._monitors is None:
            self._monitors = Monitors(self._handler)
        return self._monitors

    @property
    def profiles(self) -> Profiles:
        """Get the Profiles endpoint."""
        if self._profiles is None:
            self._profiles = Profiles(self._handler)
        return self._profiles


__all__ = ["Cert", "Errors", "Findings", "Monitors", "Profiles"]
