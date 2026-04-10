"""Domain-specific errors for the library package."""


class LibraryError(Exception):
    """Base class for all library domain errors."""


class NotFoundError(LibraryError):
    """Requested entity does not exist."""


class ValidationError(LibraryError):
    """Operation violates business rules."""


class ConflictError(LibraryError):
    """Entity already exists or state does not allow the operation."""
