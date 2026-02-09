#
# This file is part of the Generator Labs Python SDK package.
#
# (c) Generator Labs <support@generatorlabs.com>
#
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.
#

"""Tests for the pagination mixin."""

from typing import Any, Dict, List
from unittest.mock import MagicMock
from generatorlabs.api.pagination import PaginationMixin


class MockResource(PaginationMixin):
    """Mock resource class for testing pagination."""

    def __init__(self) -> None:
        self.handler = MagicMock()

    def get(self, params: Dict[str, Any] = {}) -> Dict[str, Any]:
        return {}

    def _get_resource_name(self) -> str:
        return 'hosts'


def _make_response(
    items: List[Dict[str, Any]],
    page: int,
    total_pages: int,
    total: int,
    page_size: int = 100,
) -> Dict[str, Any]:
    return {
        'total': total,
        'page': page,
        'total_pages': total_pages,
        'page_size': page_size,
        'data': items,
    }


def _make_hosts(count: int, offset: int = 0) -> List[Dict[str, Any]]:
    return [{'name': f'host_{i + offset + 1}'} for i in range(count)]


class TestPagination:
    """Test the PaginationMixin."""

    def test_get_all_single_page(self) -> None:
        """Test get_all with a single page of results."""
        resource = MockResource()
        hosts = _make_hosts(3)

        resource.get = MagicMock(return_value=_make_response(hosts, 1, 1, 3))

        result = resource.get_all()

        assert len(result) == 3
        assert result[0]['name'] == 'host_1'
        assert result[2]['name'] == 'host_3'
        resource.get.assert_called_once()

    def test_get_all_multiple_pages(self) -> None:
        """Test get_all with multiple pages of results."""
        resource = MockResource()

        def mock_get(params: Dict[str, Any] = {}) -> Dict[str, Any]:
            page = params.get('page', 1)
            if page <= 2:
                items = _make_hosts(2, (page - 1) * 2)
            else:
                items = _make_hosts(1, 4)
            return _make_response(items, page, 3, 5, 2)

        resource.get = MagicMock(side_effect=mock_get)

        result = resource.get_all(page_size=2)

        assert len(result) == 5
        assert result[0]['name'] == 'host_1'
        assert result[4]['name'] == 'host_5'
        assert resource.get.call_count == 3

    def test_get_all_empty_response(self) -> None:
        """Test get_all with no results."""
        resource = MockResource()

        resource.get = MagicMock(return_value=_make_response([], 1, 1, 0))

        result = resource.get_all()

        assert len(result) == 0
        resource.get.assert_called_once()

    def test_get_all_custom_page_size(self) -> None:
        """Test get_all passes custom page_size."""
        resource = MockResource()

        resource.get = MagicMock(
            return_value=_make_response([{'name': 'host_1'}], 1, 1, 1, 50)
        )

        result = resource.get_all(page_size=50)

        assert len(result) == 1
        call_args = resource.get.call_args[0][0]
        assert call_args['page_size'] == 50

    def test_extract_items_by_resource_name(self) -> None:
        """Test that items are extracted by resource name key."""
        resource = MockResource()

        resource.get = MagicMock(return_value={
            'total': 2,
            'page': 1,
            'total_pages': 1,
            'page_size': 100,
            'hosts': [{'name': 'a'}, {'name': 'b'}],
        })

        result = resource.get_all()

        assert len(result) == 2
        assert result[0]['name'] == 'a'
