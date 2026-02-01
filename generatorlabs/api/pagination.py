#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Pagination support for list endpoints."""

from typing import Any, Dict, List, Optional, cast


class PaginationMixin:
    """Mixin providing pagination helpers for resource classes."""

    def get_all(self, page_size: int = 100, **params: Any) -> List[Dict[str, Any]]:
        """Get all items with automatic pagination.

        Args:
            page_size: Number of items per page (default: 100)
            **params: Additional query parameters

        Returns:
            List of all items from all pages
        """
        all_items: List[Dict[str, Any]] = []
        page = 1

        while True:
            # Merge pagination params
            params_with_page = {
                **params,
                'page': page,
                'page_size': page_size
            }

            # Make the request
            response = self.get(params_with_page)  # type: ignore

            # Extract items from response
            items = self._extract_items(response)
            all_items.extend(items)

            # Check if there are more pages
            has_more = response.get('has_more', False)
            if not has_more:
                break

            page += 1

        return all_items

    def _extract_items(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract items from API response.

        Override in child class if needed.

        Args:
            response: API response dictionary

        Returns:
            List of items from response
        """
        # Try common response patterns
        resource_name = self._get_resource_name()

        if resource_name in response:
            return cast(List[Dict[str, Any]], response[resource_name])

        if 'data' in response:
            return cast(List[Dict[str, Any]], response['data'])

        if 'items' in response:
            return cast(List[Dict[str, Any]], response['items'])

        return []

    def _get_resource_name(self) -> str:
        """Get the resource name for extracting items.

        Override in child class to specify the correct resource name.

        Returns:
            Resource name (e.g., 'hosts', 'contacts')
        """
        # Default to lowercase class name
        return self.__class__.__name__.lower()
