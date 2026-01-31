#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Main client for the Generator Labs SDK."""

import re
from typing import Optional

from .exception import Exception
from .config import Config
from .api.request_handler import RequestHandler
from .api.rbl import RBL
from .api.contact import Contact
from .api.cert import Cert


class Client:
    """Generator Labs API client."""

    VERSION = "2.0.0"

    def __init__(
        self,
        account_sid: str,
        auth_token: str,
        config: Optional[Config] = None
    ) -> None:
        """Initialize the Generator Labs client.

        Args:
            account_sid: Your Generator Labs account SID
            auth_token: Your Generator Labs auth token
            config: Optional configuration object

        Raises:
            Exception: If credentials are invalid
        """
        # Validate account SID
        if not re.match(r"^[A-Z]{2}[0-9a-fA-F]{32}$", account_sid):
            raise Exception(f"Invalid account SID format: {account_sid}")

        # Validate auth token
        if not re.match(r"^[0-9a-fA-F]{64}$", auth_token):
            raise Exception(f"Invalid auth token format: {auth_token}")

        self.account_sid = account_sid
        self.auth_token = auth_token

        # Configuration
        self.config = config or Config()
        self.api_url = self.config.base_url

        # Initialize request handler
        self._handler = RequestHandler(
            account_sid,
            auth_token,
            self.api_url,
            self.config
        )

        # Lazy-loaded API namespaces
        self._rbl: Optional[RBL] = None
        self._contact: Optional[Contact] = None
        self._cert: Optional[Cert] = None

    @property
    def rbl(self) -> RBL:
        """Get the RBL monitoring API namespace.

        Returns:
            RBL namespace with endpoints for hosts, profiles, sources, etc.
        """
        if self._rbl is None:
            self._rbl = RBL(self._handler)
        return self._rbl

    @property
    def contact(self) -> Contact:
        """Get the Contact management API namespace.

        Returns:
            Contact namespace with endpoints for contacts and groups
        """
        if self._contact is None:
            self._contact = Contact(self._handler)
        return self._contact

    @property
    def cert(self) -> Cert:
        """Get the Certificate monitoring API namespace.

        Returns:
            Cert namespace with endpoints for errors, monitors, and profiles
        """
        if self._cert is None:
            self._cert = Cert(self._handler)
        return self._cert
