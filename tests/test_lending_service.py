"""Tests for LendingService checkout / return."""

import pytest

from library_catalog.exceptions import ValidationError
from library_catalog.repository import LibraryRepository
from library_catalog.services.catalog_service import CatalogService
from library_catalog.services.lending_service import LendingService
from library_catalog.services.member_service import MemberService


def test_checkout_reduces_availability_and_return_restores(
    repo: LibraryRepository,
    catalog: CatalogService,
    members: MemberService,
    lending: LendingService,
) -> None:
    book = catalog.add_book(
        title="Loan Me",
        author="Author",
        isbn="9780000000001",
        copies=2,
    )
    member = members.register(name="Reader", email="r@example.com", max_loans=5)
    assert book.copies_available == 2

    loan = lending.checkout(book_id=book.id, member_id=member.id, loan_days=7)
    updated = catalog.get_book(book.id)
    assert updated.copies_available == 1

    lending.return_book(loan_id=loan.id)
    again = catalog.get_book(book.id)
    assert again.copies_available == 2


def test_max_concurrent_loans_enforced(
    catalog: CatalogService,
    members: MemberService,
    lending: LendingService,
) -> None:
    b1 = catalog.add_book(title="B1", author="A", isbn="9780000000001", copies=2)
    b2 = catalog.add_book(title="B2", author="A", isbn="9780000000002", copies=1)
    m = members.register(name="Limited", email="lim@example.com", max_loans=1)
    lending.checkout(book_id=b1.id, member_id=m.id, loan_days=7)
    with pytest.raises(ValidationError, match="maximum"):
        lending.checkout(book_id=b2.id, member_id=m.id, loan_days=7)
