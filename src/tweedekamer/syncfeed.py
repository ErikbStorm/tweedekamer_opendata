"""SyncFeed API client for incremental synchronisation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from types import TracebackType
from typing import Any
from urllib.parse import parse_qs, urlparse
from uuid import UUID

import httpx
from lxml import etree

from tweedekamer._http import (
    DEFAULT_SYNCFEED_BASE,
    DEFAULT_TIMEOUT,
    default_user_agent,
    ensure_client,
    raise_for_status,
)
from tweedekamer._version import __version__

ATOM_NS = "http://www.w3.org/2005/Atom"
TK_NS = "http://www.tweedekamer.nl/xsd/tkData/v1-0"

NS = {
    "atom": ATOM_NS,
    "tk": TK_NS,
}


def _local(tag: str) -> str:
    if "}" in tag:
        return tag.rsplit("}", 1)[-1]
    return tag


def _is_nil(el: etree._Element) -> bool:
    for key, value in el.attrib.items():
        if _local(key) == "nil" and str(value).lower() == "true":
            return True
    return False


def _element_to_dict(el: etree._Element) -> dict[str, Any] | Any:
    """Convert a SyncFeed XML payload element into a nested dict (or scalar/None)."""
    children = list(el)
    text = (el.text or "").strip()

    # Leaf with xsi:nil
    if not children and _is_nil(el):
        return None

    result: dict[str, Any] = {}
    for key, value in el.attrib.items():
        attr = _local(key)
        if attr == "nil":
            continue
        if value in ("true", "false"):
            result[attr] = value == "true"
        else:
            result[attr] = value

    if not children:
        if text:
            if result:
                result["value"] = text
                return result
            return text
        return result

    for child in children:
        name = _local(child.tag)
        value = _element_to_dict(child)

        if name in result:
            existing = result[name]
            if not isinstance(existing, list):
                result[name] = [existing]
            result[name].append(value)
        else:
            result[name] = value
    return result


@dataclass
class FeedEntry:
    """A single Atom entry from the SyncFeed."""

    id: str
    title: str | None
    updated: datetime | None
    category: str | None
    entity_url: str | None
    next_link: str | None
    payload: dict[str, Any] = field(default_factory=dict)
    raw_xml: str | None = None

    @property
    def entity_id(self) -> UUID | None:
        """Best-effort GUID of the entity."""
        if "id" in self.payload:
            try:
                return UUID(str(self.payload["id"]))
            except ValueError:
                return None
        # fallback: last path segment of entry id URL
        try:
            return UUID(self.id.rstrip("/").rsplit("/", 1)[-1])
        except ValueError:
            return None


@dataclass
class FeedPage:
    """One page of the SyncFeed."""

    title: str | None
    updated: datetime | None
    self_link: str | None
    next_link: str | None
    entries: list[FeedEntry]

    @property
    def skip_token(self) -> str | None:
        """Extract ``skiptoken`` from the next-page link, if present."""
        if not self.next_link:
            return None
        query = parse_qs(urlparse(self.next_link).query)
        tokens = query.get("skiptoken") or query.get("skipToken")
        return tokens[0] if tokens else None


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    # Atom timestamps are ISO-8601; handle trailing Z
    text = value.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def parse_feed(xml_bytes: bytes) -> FeedPage:
    """Parse a SyncFeed Atom document into a :class:`FeedPage`."""
    root = etree.fromstring(xml_bytes)

    def find_text(path: str) -> str | None:
        el = root.find(path, NS)
        if el is None or el.text is None:
            return None
        return el.text

    def find_link(rel: str) -> str | None:
        for link in root.findall("atom:link", NS):
            if link.get("rel") == rel:
                return link.get("href")
        return None

    entries: list[FeedEntry] = []
    for entry_el in root.findall("atom:entry", NS):
        entry_id = entry_el.findtext("atom:id", default="", namespaces=NS) or ""
        title = entry_el.findtext("atom:title", default=None, namespaces=NS)
        updated = _parse_datetime(entry_el.findtext("atom:updated", default=None, namespaces=NS))
        cat_el = entry_el.find("atom:category", NS)
        category = cat_el.get("term") if cat_el is not None else None

        next_link = None
        entity_url = entry_id or None
        for link in entry_el.findall("atom:link", NS):
            if link.get("rel") == "next":
                next_link = link.get("href")

        payload: dict[str, Any] = {}
        raw_xml = None
        content = entry_el.find("atom:content", NS)
        if content is not None and len(content):
            payload_el = content[0]
            raw_xml = etree.tostring(payload_el, encoding="unicode")
            parsed = _element_to_dict(payload_el)
            payload = parsed if isinstance(parsed, dict) else {"value": parsed}
            # lift common tk attributes
            if "id" not in payload and payload_el.get("id"):
                payload["id"] = payload_el.get("id")

        entries.append(
            FeedEntry(
                id=entry_id,
                title=title,
                updated=updated,
                category=category,
                entity_url=entity_url,
                next_link=next_link,
                payload=payload,
                raw_xml=raw_xml,
            )
        )

    return FeedPage(
        title=find_text("atom:title"),
        updated=_parse_datetime(find_text("atom:updated")),
        self_link=find_link("self"),
        next_link=find_link("next"),
        entries=entries,
    )


class SyncFeedClient:
    """Client for the Tweede Kamer SyncFeed API (Atom-based incremental sync).

    Example:
        >>> from tweedekamer import SyncFeedClient
        >>> with SyncFeedClient() as feed:
        ...     page = feed.fetch(category="Persoon")
        ...     token = page.skip_token
    """

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_SYNCFEED_BASE,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str | None = None,
        http_client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._headers = {
            "User-Agent": user_agent or default_user_agent(__version__),
            "Accept": "application/atom+xml, application/xml, text/xml, */*",
        }
        self._http, self._owns_client = ensure_client(
            http_client,
            timeout=timeout,
            headers=self._headers,
        )

    def close(self) -> None:
        if self._owns_client:
            self._http.close()

    def __enter__(self) -> SyncFeedClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def fetch(
        self,
        *,
        category: str | None = None,
        skiptoken: str | None = None,
    ) -> FeedPage:
        """Fetch one page of the change feed.

        Args:
            category: Optional entity category filter (e.g. ``\"Zaak\"``, ``\"Persoon\"``).
            skiptoken: Continuation token from a previous page's ``skip_token``.
        """
        params: dict[str, str] = {}
        if category:
            params["category"] = category
        if skiptoken:
            params["skiptoken"] = skiptoken

        response = self._http.get(f"{self.base_url}/Feed", params=params or None)
        raise_for_status(response)
        return parse_feed(response.content)

    def fetch_url(self, url: str) -> FeedPage:
        """Fetch a feed page by absolute next-link URL."""
        response = self._http.get(url)
        raise_for_status(response)
        return parse_feed(response.content)

    def get_entity(self, entity_id: UUID | str) -> bytes:
        """Download the XML body of a single entity by id."""
        response = self._http.get(f"{self.base_url}/Entiteiten/{entity_id}")
        raise_for_status(response)
        return response.content

    def get_entity_parsed(self, entity_id: UUID | str) -> dict[str, Any]:
        """Download and parse a single entity as a dict."""
        raw = self.get_entity(entity_id)
        root = etree.fromstring(raw)
        # response may be the entity element directly or wrapped
        return _element_to_dict(root)

    def download_resource(
        self,
        entity_id: UUID | str,
        *,
        path: str | None = None,
    ) -> bytes:
        """Download the binary resource for an entity (SyncFeed Resources endpoint)."""
        response = self._http.get(f"{self.base_url}/Resources/{entity_id}")
        raise_for_status(response)
        content = response.content
        if path is not None:
            with open(path, "wb") as fh:
                fh.write(content)
        return content

    def iterate(
        self,
        *,
        category: str | None = None,
        skiptoken: str | None = None,
        max_pages: int | None = None,
    ):
        """Yield :class:`FeedEntry` items across pages.

        Args:
            category: Optional category filter.
            skiptoken: Start token.
            max_pages: Stop after this many feed pages (``None`` = unlimited).
        """
        pages = 0
        page = self.fetch(category=category, skiptoken=skiptoken)
        while True:
            pages += 1
            yield from page.entries
            if not page.next_link:
                break
            if max_pages is not None and pages >= max_pages:
                break
            page = self.fetch_url(page.next_link)
