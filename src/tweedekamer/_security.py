"""Client-side safety helpers (URL allowlisting, UUID validation, safe XML)."""

from __future__ import annotations

from urllib.parse import urljoin, urlparse
from uuid import UUID

from lxml import etree

from tweedekamer.exceptions import SecurityError


def require_entity_id(entity_id: UUID | str) -> str:
    """Validate and normalise an entity GUID.

    Raises:
        SecurityError: If ``entity_id`` is not a valid UUID.
    """
    try:
        return str(UUID(str(entity_id)))
    except (ValueError, AttributeError, TypeError) as exc:
        raise SecurityError(f"entity_id must be a UUID, got {entity_id!r}") from exc


def _origin(url: str) -> tuple[str, str, int | None]:
    """Return (scheme, hostname lowercased, port) for comparison."""
    parsed = urlparse(url)
    scheme = (parsed.scheme or "").lower()
    host = (parsed.hostname or "").lower()
    port = parsed.port
    if port is None and scheme == "https":
        port = 443
    elif port is None and scheme == "http":
        port = 80
    return scheme, host, port


def assert_url_allowed(url: str, *, allowed_base: str, purpose: str = "request") -> str:
    """Ensure ``url`` targets the same origin as ``allowed_base``.

    Relative URLs are resolved against ``allowed_base``.

    Raises:
        SecurityError: If the host/scheme/port do not match the configured base.
    """
    if not url or not str(url).strip():
        raise SecurityError(f"Refusing empty URL for {purpose}")

    absolute = urljoin(allowed_base.rstrip("/") + "/", url)
    base_origin = _origin(allowed_base)
    target_origin = _origin(absolute)

    if not target_origin[1]:
        raise SecurityError(f"Refusing URL without host for {purpose}: {url!r}")

    if target_origin != base_origin:
        raise SecurityError(
            f"Refusing {purpose} URL with host {target_origin[1]!r} "
            f"(allowed origin host {base_origin[1]!r}): {absolute}"
        )

    if target_origin[0] not in ("http", "https"):
        raise SecurityError(f"Refusing non-HTTP(S) URL for {purpose}: {absolute}")

    return absolute


def safe_xml_parser() -> etree.XMLParser:
    """Return an XML parser that rejects external entities and network access."""
    return etree.XMLParser(
        resolve_entities=False,
        no_network=True,
        huge_tree=False,
        load_dtd=False,
        dtd_validation=False,
    )


def parse_xml(xml_bytes: bytes) -> etree._Element:
    """Parse XML bytes with hardened defaults (no XXE / external DTD)."""
    if not xml_bytes:
        raise SecurityError("Refusing to parse empty XML document")
    try:
        return etree.fromstring(xml_bytes, parser=safe_xml_parser())
    except etree.XMLSyntaxError as exc:
        raise SecurityError(f"Invalid XML: {exc}") from exc
