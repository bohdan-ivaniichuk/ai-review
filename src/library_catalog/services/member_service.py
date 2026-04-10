"""Register and fetch members."""

from __future__ import annotations

from typing import List
from uuid import UUID

from library_catalog.exceptions import ConflictError, NotFoundError, ValidationError
from library_catalog.models import Member, new_member_id
from library_catalog.repository import LibraryRepository


class MemberService:
    def __init__(self, repo: LibraryRepository) -> None:
        self._repo = repo

    def register(self, *, name: str, email: str, max_loans: int = 5) -> Member:
        name = name.strip()
        email = email.strip().lower()
        if not name:
            raise ValidationError("name is required")
        if "@" not in email:
            raise ValidationError("valid email is required")
        if max_loans < 1:
            raise ValidationError("max_loans must be at least 1")
        if self._repo.member_by_email(email):
            raise ConflictError("member with this email already exists")

        member = Member(
            id=new_member_id(),
            name=name,
            email=email,
            max_concurrent_loans=max_loans,
        )
        self._repo.save_member(member)
        return member

    def get(self, member_id: UUID) -> Member:
        member = self._repo.get_member(member_id)
        if member is None:
            raise NotFoundError("member not found")
        return member

    def list_members(self) -> List[Member]:
        return sorted(self._repo.all_members(), key=lambda m: m.name.lower())
