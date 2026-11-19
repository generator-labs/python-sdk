#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Account API endpoints."""

from typing import Any, Dict, Optional
from .request_handler import RequestHandler
from ..response import Response


class Account:
    """Account namespace: the account, its balance, its usage and its scheduled checks."""

    def __init__(self, handler: RequestHandler) -> None:
        """Initialize the Account namespace.

        Args:
            handler: The request handler instance
        """
        self.handler = handler

    def get(self, **options: Any) -> Response:
        """Get the account: its balance, whether its checks are running, and plan usage.

        Args:
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with the account
        """
        return self.handler.get("account", **options)

    def balance(self, **options: Any) -> float:
        """Get the account balance.

        Args:
            **options: Request options (request_id)

        Returns:
            The account balance
        """
        return float(self.handler.get_plain("account/balance", **options))

    def usage(self, params: Optional[Dict[str, Any]] = None, **options: Any) -> Response:
        """Get the account's usage by month.

        Args:
            params: Optional query parameters (months)
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response with the usage of each month
        """
        return self.handler.get("account/usage", params or {}, **options)

    def pause_checks(self, **options: Any) -> Response:
        """Pause the account's scheduled checks.

        Args:
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.post("account/checks/pause", **options)

    def resume_checks(self, **options: Any) -> Response:
        """Resume the account's scheduled checks.

        Args:
            **options: Request options (idempotency_key, request_id, if_none_match, fields)

        Returns:
            API response
        """
        return self.handler.post("account/checks/resume", **options)
