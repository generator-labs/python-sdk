#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Exception classes for the Generator Labs SDK."""

import builtins
from typing import Any, Optional


class Exception(builtins.Exception):
    """Base exception for all Generator Labs SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: Any = None,
        request_id: Optional[str] = None
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.request_id = request_id
