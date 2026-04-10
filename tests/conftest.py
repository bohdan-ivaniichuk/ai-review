"""Shared fixtures for library_catalog tests."""

import pytest

from library_catalog.repository import LibraryRepository
from library_catalog.services.catalog_service import CatalogService
from library_catalog.services.lending_service import LendingService
from library_catalog.services.member_service import MemberService


@pytest.fixture
def repo() -> LibraryRepository:
    return LibraryRepository()


@pytest.fixture
def catalog(repo: LibraryRepository) -> CatalogService:
    return CatalogService(repo)


@pytest.fixture
def members(repo: LibraryRepository) -> MemberService:
    return MemberService(repo)


@pytest.fixture
def lending(repo: LibraryRepository) -> LendingService:
    return LendingService(repo)
