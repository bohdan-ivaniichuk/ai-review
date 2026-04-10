"""Borrow, return, and overdue reporting."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List
from uuid import UUID

from library_catalog.exceptions import NotFoundError, ValidationError
from library_catalog.models import Book, Loan, default_borrowed_at, new_loan_id
from library_catalog.repository import LibraryRepository


DEFAULT_LOAN_DAYS = 21


class LendingService:
    def __init__(self, repo: LibraryRepository) -> None:
        self._repo = repo

    def checkout(
        self,
        *,
        book_id: UUID,
        member_id: UUID,
        loan_days: int = DEFAULT_LOAN_DAYS,
    ) -> Loan:
        if loan_days < 1:
            raise ValidationError("loan_days must be at least 1")

        book = self._repo.get_book(book_id)
        if book is None:
            raise NotFoundError("book not found")
        member = self._repo.get_member(member_id)
        if member is None:
            raise NotFoundError("member not found")

        active_for_member = [
            ln for ln in self._repo.loans_for_member(member_id) if ln.is_active
        ]
        if len(active_for_member) >= member.max_concurrent_loans:
            raise ValidationError("member has reached the maximum number of active loans")

        if book.copies_available < 1:
            raise ValidationError("no copies available to borrow")

        borrowed = default_borrowed_at()
        due = (borrowed + timedelta(days=loan_days)).date()

        loan = Loan(
            id=new_loan_id(),
            book_id=book_id,
            member_id=member_id,
            borrowed_at=borrowed,
            due_date=due,
        )
        self._repo.save_loan(loan)

        updated = Book(
            id=book.id,
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            copies_total=book.copies_total,
            copies_available=book.copies_available - 1,
        )
        self._repo.replace_book(updated)
        return loan

    def return_book(self, *, loan_id: UUID) -> Loan:
        loan = self._repo.get_loan(loan_id)
        if loan is None:
            raise NotFoundError("loan not found")
        if not loan.is_active:
            raise ValidationError("loan is already returned")

        book = self._repo.get_book(loan.book_id)
        if book is None:
            raise NotFoundError("book not found")

        returned = Loan(
            id=loan.id,
            book_id=loan.book_id,
            member_id=loan.member_id,
            borrowed_at=loan.borrowed_at,
            due_date=loan.due_date,
            returned_at=datetime.now(),
        )
        self._repo.save_loan(returned)

        updated = Book(
            id=book.id,
            title=book.title,
            author=book.author,
            isbn=book.isbn,
            copies_total=book.copies_total,
            copies_available=min(book.copies_total, book.copies_available + 1),
        )
        self._repo.replace_book(updated)
        return returned

    def overdue_loans(self) -> List[Loan]:
        return [ln for ln in self._repo.all_active_loans() if ln.is_overdue]
