"""Application exception hierarchy. Internal messages are logged; clients get generic detail."""


class AppError(Exception):
    """Base for app errors. Subclasses define stable status_code and generic client detail."""

    status_code: int = 500
    detail: str = "Internal server error"

    def __init__(self, message: str = "") -> None:
        super().__init__(message)


class NotFoundError(AppError):
    """Resource not found (404)."""

    status_code = 404
    detail = "Resource not found"


class ConflictError(AppError):
    """Conflict with existing resource (409)."""

    status_code = 409
    detail = "Conflict with existing resource"
