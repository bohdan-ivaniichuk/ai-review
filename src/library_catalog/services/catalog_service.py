"""Register and query books."""

from __future__ import annotations

from typing import List
from uuid import UUID

from library_catalog.exceptions import ConflictError, NotFoundError, ValidationError
from library_catalog.models import Book, new_book_id
from library_catalog.repository import LibraryRepository


class CatalogService:
    def __init__(self, repo: LibraryRepository) -> None:
        self._repo = repo

    def add_book(
        self,
        *,
        title: str,
        author: str,
        isbn: str,
        copies: int,
    ) -> Book:
        title = title.strip()
        author = author.strip()
        isbn = _normalize_isbn(isbn)
        if not title or not author or not isbn:
            raise ValidationError("title, author, and isbn are required")
        if len(isbn) not in (10, 13):
            raise ValidationError("ISBN must be 10 or 13 characters (after normalizing digits/X)")
        if copies < 1:
            raise ValidationError("copies must be at least 1")
        if self._repo.books_by_isbn(isbn):
            raise ConflictError(f"book with ISBN {isbn} already exists")

        book = Book(
            id=new_book_id(),
            title=title,
            author=author,
            isbn=isbn,
            copies_total=copies,
            copies_available=copies,
        )
        self._repo.save_book(book)
        return book

    def get_book(self, book_id: UUID) -> Book:
        book = self._repo.get_book(book_id)
        if book is None:
            raise NotFoundError("book not found")
        return book

    def list_books(self) -> List[Book]:
        return sorted(self._repo.all_books(), key=lambda b: (b.title.lower(), b.author.lower()))

    def search_books(self, query: str) -> List[Book]:
        """Return books whose title or author contains the query (case-insensitive)."""
        q = query.strip().lower()
        if not q:
            return self.list_books()
        matches = [
            b
            for b in self._repo.all_books()
            if q in b.title.lower() or q in b.author.lower()
        ]
        return sorted(matches, key=lambda b: (b.title.lower(), b.author.lower()))


def _normalize_isbn(raw: str) -> str:
    return "".join(ch for ch in raw.strip() if ch.isdigit() or ch.upper() == "X")
