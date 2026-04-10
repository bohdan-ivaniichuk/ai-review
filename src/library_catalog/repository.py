"""In-memory persistence for books, members, and loans."""

from __future__ import annotations

from typing import Dict, Iterable, List, Optional
from uuid import UUID

from library_catalog.models import Book, Loan, Member


class LibraryRepository:
    """Thread-unsafe in-memory store (fine for CLI / tests)."""

    def __init__(self) -> None:
        self._books: Dict[UUID, Book] = {}
        self._members: Dict[UUID, Member] = {}
        self._loans: Dict[UUID, Loan] = {}

    # Books
    def save_book(self, book: Book) -> None:
        self._books[book.id] = book

    def get_book(self, book_id: UUID) -> Optional[Book]:
        return self._books.get(book_id)

    def books_by_isbn(self, isbn: str) -> List[Book]:
        return [b for b in self._books.values() if b.isbn == isbn]

    def all_books(self) -> Iterable[Book]:
        return self._books.values()

    def replace_book(self, book: Book) -> None:
        self._books[book.id] = book

    # Members
    def save_member(self, member: Member) -> None:
        self._members[member.id] = member

    def get_member(self, member_id: UUID) -> Optional[Member]:
        return self._members.get(member_id)

    def member_by_email(self, email: str) -> Optional[Member]:
        normalized = email.strip().lower()
        for m in self._members.values():
            if m.email.strip().lower() == normalized:
                return m
        return None

    def all_members(self) -> Iterable[Member]:
        return self._members.values()

    # Loans
    def save_loan(self, loan: Loan) -> None:
        self._loans[loan.id] = loan

    def get_loan(self, loan_id: UUID) -> Optional[Loan]:
        return self._loans.get(loan_id)

    def loans_for_member(self, member_id: UUID) -> List[Loan]:
        return [ln for ln in self._loans.values() if ln.member_id == member_id]

    def active_loans_for_book(self, book_id: UUID) -> List[Loan]:
        return [
            ln
            for ln in self._loans.values()
            if ln.book_id == book_id and ln.is_active
        ]

    def all_active_loans(self) -> List[Loan]:
        return [ln for ln in self._loans.values() if ln.is_active]
