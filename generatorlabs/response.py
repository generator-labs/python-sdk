#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Response wrapper with rate limit information."""

from typing import Any, Dict, Iterator, Optional


class RateLimitInfo:
    """Rate limit information from API response headers."""

    def __init__(self, limit: str, remaining: int, reset: int) -> None:
        self.limit = limit
        self.remaining = remaining
        self.reset = reset

    def __repr__(self) -> str:
        return f"RateLimitInfo(limit={self.limit!r}, remaining={self.remaining}, reset={self.reset})"


class Response:
    """API response wrapper providing dict-like access to response data and rate limit info.

    Supports bracket notation (response['key']) for backward compatibility
    with raw dict returns, while also exposing rate_limit_info.
    """

    def __init__(self, data: Dict[str, Any], rate_limit_info: Optional[RateLimitInfo] = None) -> None:
        self._data = data
        self.rate_limit_info = rate_limit_info

    def __getitem__(self, key: str) -> Any:
        return self._data[key]

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Response({self._data!r}, rate_limit_info={self.rate_limit_info!r})"

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def keys(self) -> Any:
        return self._data.keys()

    def values(self) -> Any:
        return self._data.values()

    def items(self) -> Any:
        return self._data.items()

    def to_dict(self) -> Dict[str, Any]:
        return self._data.copy()
