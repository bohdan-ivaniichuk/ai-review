"""Command-line interface for the library catalog."""

from __future__ import annotations

import argparse
import sys
from uuid import UUID

from library_catalog.exceptions import LibraryError
from library_catalog.repository import LibraryRepository
from library_catalog.services.catalog_service import CatalogService
from library_catalog.services.lending_service import LendingService
from library_catalog.services.member_service import MemberService


def _services() -> tuple[CatalogService, MemberService, LendingService]:
    repo = LibraryRepository()
    return (
        CatalogService(repo),
        MemberService(repo),
        LendingService(repo),
    )


def _run_demo() -> int:
    """Single-process walkthrough (state is not persisted between CLI invocations)."""
    repo = LibraryRepository()
    catalog = CatalogService(repo)
    members = MemberService(repo)
    lending = LendingService(repo)

    b1 = catalog.add_book(
        title="Designing Data-Intensive Applications",
        author="Martin Kleppmann",
        isbn="9781449373320",
        copies=2,
    )
    m1 = members.register(name="Ada Lovelace", email="ada@example.com", max_loans=3)
    loan = lending.checkout(book_id=b1.id, member_id=m1.id, loan_days=14)
    print(f"Book '{b1.title}' loaned to {m1.name}; loan {loan.id}, due {loan.due_date}")
    returned = lending.return_book(loan_id=loan.id)
    print(f"Returned: {returned.returned_at is not None}")
    books = catalog.list_books()
    print(f"Catalog has {len(books)} title(s); available copies: {books[0].copies_available}")
    return 0


_STATELESS = (
    "State is only in memory and is not saved between process runs; "
    "use `demo` for a full flow, or wire persistence yourself."
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="library-catalog",
        description=f"In-memory library management. {_STATELESS}",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("demo", help="Run a one-shot in-memory demo (no persistence)")

    p_books = sub.add_parser("books", help=f"List or add books. {_STATELESS}")
    p_books_sub = p_books.add_subparsers(dest="books_cmd", required=True)
    p_books_sub.add_parser("list", help="List all books")
    p_books_add = p_books_sub.add_parser("add", help="Add a book")
    p_books_add.add_argument("--title", required=True)
    p_books_add.add_argument("--author", required=True)
    p_books_add.add_argument("--isbn", required=True)
    p_books_add.add_argument("--copies", type=int, default=1)

    p_mem = sub.add_parser("members", help=f"Register or list members. {_STATELESS}")
    p_mem_sub = p_mem.add_subparsers(dest="mem_cmd", required=True)
    p_mem_sub.add_parser("list", help="List members")
    p_mem_reg = p_mem_sub.add_parser("register", help="Register a member")
    p_mem_reg.add_argument("--name", required=True)
    p_mem_reg.add_argument("--email", required=True)
    p_mem_reg.add_argument("--max-loans", type=int, default=5)

    p_loans = sub.add_parser("loans", help=f"Checkout, return, or list overdue. {_STATELESS}")
    p_loans_sub = p_loans.add_subparsers(dest="loans_cmd", required=True)
    p_co = p_loans_sub.add_parser("checkout", help="Borrow a book")
    p_co.add_argument("--book-id", type=UUID, required=True)
    p_co.add_argument("--member-id", type=UUID, required=True)
    p_co.add_argument("--days", type=int, default=21)
    p_ret = p_loans_sub.add_parser("return", help="Return a book")
    p_ret.add_argument("--loan-id", type=UUID, required=True)
    p_od = p_loans_sub.add_parser("overdue", help="List overdue active loans")

    args = parser.parse_args(argv)

    if args.cmd == "demo":
        return _run_demo()

    catalog, members, lending = _services()

    try:
        if args.cmd == "books" and args.books_cmd == "list":
            for b in catalog.list_books():
                print(
                    f"{b.id}\t{b.title}\t{b.author}\t{b.isbn}\t"
                    f"available {b.copies_available}/{b.copies_total}"
                )
            return 0
        if args.cmd == "books" and args.books_cmd == "add":
            book = catalog.add_book(
                title=args.title,
                author=args.author,
                isbn=args.isbn,
                copies=args.copies,
            )
            print(f"Added book {book.id}")
            return 0
        if args.cmd == "members" and args.mem_cmd == "list":
            for m in members.list_members():
                print(f"{m.id}\t{m.name}\t{m.email}\tmax_loans={m.max_concurrent_loans}")
            return 0
        if args.cmd == "members" and args.mem_cmd == "register":
            m = members.register(name=args.name, email=args.email, max_loans=args.max_loans)
            print(f"Registered member {m.id}")
            return 0
        if args.cmd == "loans" and args.loans_cmd == "checkout":
            loan = lending.checkout(
                book_id=args.book_id,
                member_id=args.member_id,
                loan_days=args.days,
            )
            print(f"Loan {loan.id} due {loan.due_date.isoformat()}")
            return 0
        if args.cmd == "loans" and args.loans_cmd == "return":
            loan = lending.return_book(loan_id=args.loan_id)
            print(f"Returned loan {loan.id}")
            return 0
        if args.cmd == "loans" and args.loans_cmd == "overdue":
            overdue = lending.overdue_loans()
            if not overdue:
                print("No overdue loans.")
                return 0
            for ln in overdue:
                print(f"{ln.id}\tbook={ln.book_id}\tmember={ln.member_id}\tdue={ln.due_date.isoformat()}")
            return 0
    except LibraryError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 1
