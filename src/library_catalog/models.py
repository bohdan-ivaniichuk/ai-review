"""Core entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4


def _utcnow() -> datetime:
    return datetime.now(tz=None)


@dataclass(frozen=True)
class Book:
    """A title the library can lend."""

    id: UUID
    title: str
    author: str
    isbn: str
    copies_total: int
    copies_available: int

    def __post_init__(self) -> None:
        if self.copies_total < 1:
            raise ValueError("copies_total must be at least 1")
        if not (0 <= self.copies_available <= self.copies_total):
            raise ValueError("copies_available must be within [0, copies_total]")


@dataclass(frozen=True)
class Member:
    """Registered borrower."""

    id: UUID
    name: str
    email: str
    max_concurrent_loans: int = 5

    def __post_init__(self) -> None:
        if self.max_concurrent_loans < 1:
            raise ValueError("max_concurrent_loans must be at least 1")


@dataclass
class Loan:
    """An active or completed loan."""

    id: UUID
    book_id: UUID
    member_id: UUID
    borrowed_at: datetime
    due_date: date
    returned_at: Optional[datetime] = None

    @property
    def is_active(self) -> bool:
        return self.returned_at is None

    @property
    def is_overdue(self) -> bool:
        if not self.is_active:
            return False
        return date.today() > self.due_date


def new_book_id() -> UUID:
    return uuid4()


def new_member_id() -> UUID:
    return uuid4()


def new_loan_id() -> UUID:
    return uuid4()


def default_borrowed_at() -> datetime:
    return _utcnow()
