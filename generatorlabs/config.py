#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Configuration options for the Generator Labs SDK."""

from typing import Optional


class Config:
    """Configuration options for the Generator Labs API client.

    Args:
        timeout: Request timeout in seconds (default: 30)
        connect_timeout: Connection timeout in seconds (default: 5)
        max_retries: Maximum number of retry attempts (default: 3)
        retry_backoff: Backoff multiplier for retries (default: 1)
        base_url: Custom API base URL (default: https://api.generatorlabs.com/4.0/)
    """

    def __init__(
        self,
        timeout: float = 30.0,
        connect_timeout: float = 5.0,
        max_retries: int = 3,
        retry_backoff: float = 1.0,
        base_url: Optional[str] = None
    ) -> None:
        """Initialize configuration."""
        self.timeout = timeout
        self.connect_timeout = connect_timeout
        self.max_retries = max_retries
        self.retry_backoff = retry_backoff
        self.base_url = base_url or "https://api.generatorlabs.com/4.0/"
