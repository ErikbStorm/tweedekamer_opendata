"""Exception types raised by the Tweede Kamer client."""

from __future__ import annotations

from typing import Any


class TweedekamerError(Exception):
    """Base error for all library failures."""


class HTTPError(TweedekamerError):
    """The remote API returned a non-success HTTP status."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        url: str | None = None,
        body: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.url = url
        self.body = body

    def __str__(self) -> str:
        parts = [super().__str__()]
        if self.status_code is not None:
            parts.append(f"status={self.status_code}")
        if self.url:
            parts.append(f"url={self.url}")
        return " | ".join(parts)


class NotFoundError(HTTPError):
    """The requested entity was not found (HTTP 404)."""


class QueryError(TweedekamerError):
    """Raised when a query cannot be constructed or executed."""

    def __init__(self, message: str, *, details: Any = None) -> None:
        super().__init__(message)
        self.details = details
