"""Tests for CatalogService."""

import pytest

from library_catalog.exceptions import ConflictError, ValidationError
from library_catalog.repository import LibraryRepository
from library_catalog.services.catalog_service import CatalogService


def test_add_book_and_list_sorted(catalog: CatalogService) -> None:
    b2 = catalog.add_book(
        title="Zebra Tales",
        author="Alice Author",
        isbn="9780000000002",
        copies=1,
    )
    b1 = catalog.add_book(
        title="Alpha Guide",
        author="Bob Writer",
        isbn="9780000000001",
        copies=3,
    )
    books = catalog.list_books()
    assert [x.id for x in books] == [b1.id, b2.id]


def test_duplicate_isbn_conflict(catalog: CatalogService) -> None:
    catalog.add_book(title="A", author="B", isbn="9780000000001", copies=1)
    with pytest.raises(ConflictError, match="ISBN"):
        catalog.add_book(title="C", author="D", isbn="9780000000001", copies=1)


def test_invalid_isbn_length(catalog: CatalogService) -> None:
    with pytest.raises(ValidationError, match="10 or 13"):
        catalog.add_book(title="A", author="B", isbn="12345", copies=1)


def test_search_by_author_substring(catalog: CatalogService) -> None:
    catalog.add_book(title="Vol1", author="Martin Kleppmann", isbn="9781449373320", copies=2)
    catalog.add_book(title="Other", author="Jane Doe", isbn="9780000000001", copies=1)
    found = catalog.search_books("kleppmann")
    assert len(found) == 1
    assert found[0].title == "Vol1"


def test_search_empty_query_returns_full_list(catalog: CatalogService) -> None:
    catalog.add_book(title="A", author="B", isbn="9780000000001", copies=1)
    assert len(catalog.search_books("   ")) == len(catalog.list_books())
