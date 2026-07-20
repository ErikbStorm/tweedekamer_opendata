"""Unit tests for the SyncFeed client."""

from __future__ import annotations

from pathlib import Path

import httpx
import respx

from tweedekamer import SyncFeedClient
from tweedekamer.syncfeed import parse_feed

SYNCFEED = "https://gegevensmagazijn.tweedekamer.nl/SyncFeed/2.0"

SAMPLE_FEED = b"""<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:tk="http://www.tweedekamer.nl/xsd/tkData/v1-0">
  <title>Gegevensmagazijn SyncFeed (category: Persoon)</title>
  <link rel="self" href="https://gegevensmagazijn.tweedekamer.nl/SyncFeed/2.0/Feed?category=Persoon" />
  <link rel="next" href="https://gegevensmagazijn.tweedekamer.nl/SyncFeed/2.0/Feed?skiptoken=99&amp;category=Persoon" />
  <updated>2026-07-19T12:00:00Z</updated>
  <id>https://gegevensmagazijn.tweedekamer.nl/SyncFeed/2.0/Feed?category=Persoon</id>
  <entry>
    <title>77dc181f-00d6-4d5e-b188-3fd0c02f4006</title>
    <id>https://gegevensmagazijn.tweedekamer.nl/SyncFeed/2.0/Entiteiten/77dc181f-00d6-4d5e-b188-3fd0c02f4006</id>
    <updated>2023-08-29T11:10:11.0962032Z</updated>
    <category term="persoon" />
    <content type="application/xml">
      <persoon xmlns="http://www.tweedekamer.nl/xsd/tkData/v1-0"
               xmlns:tk="http://www.tweedekamer.nl/xsd/tkData/v1-0"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               id="77dc181f-00d6-4d5e-b188-3fd0c02f4006"
               tk:bijgewerkt="2023-08-29T11:09:44Z"
               tk:verwijderd="false">
        <nummer>8</nummer>
        <achternaam>Savornin Lohman</achternaam>
        <roepnaam xsi:nil="true" />
        <functie>Oud Kamerlid</functie>
      </persoon>
    </content>
  </entry>
</feed>
"""


def test_parse_feed():
    page = parse_feed(SAMPLE_FEED)
    assert page.title and "Persoon" in page.title
    assert page.skip_token == "99"
    assert page.next_link is not None
    assert len(page.entries) == 1
    entry = page.entries[0]
    assert entry.category == "persoon"
    assert entry.payload["achternaam"] == "Savornin Lohman"
    assert entry.payload["verwijderd"] is False
    assert entry.payload.get("roepnaam") is None
    assert str(entry.entity_id) == "77dc181f-00d6-4d5e-b188-3fd0c02f4006"


@respx.mock
def test_fetch_category():
    respx.get(f"{SYNCFEED}/Feed").mock(return_value=httpx.Response(200, content=SAMPLE_FEED))
    with SyncFeedClient() as client:
        page = client.fetch(category="Persoon")
    assert len(page.entries) == 1
    assert respx.calls.last.request.url.params["category"] == "Persoon"


@respx.mock
def test_fetch_with_skiptoken():
    respx.get(f"{SYNCFEED}/Feed").mock(return_value=httpx.Response(200, content=SAMPLE_FEED))
    with SyncFeedClient() as client:
        client.fetch(category="Zaak", skiptoken="123")
    params = respx.calls.last.request.url.params
    assert params["category"] == "Zaak"
    assert params["skiptoken"] == "123"


@respx.mock
def test_download_resource(tmp_path: Path):
    payload = b"%PDF-1.4 fake"
    entity_id = "77dc181f-00d6-4d5e-b188-3fd0c02f4006"
    respx.get(f"{SYNCFEED}/Resources/{entity_id}").mock(
        return_value=httpx.Response(200, content=payload)
    )
    out = tmp_path / "doc.pdf"
    with SyncFeedClient() as client:
        data = client.download_resource(entity_id, path=str(out))
    assert data == payload
    assert out.read_bytes() == payload


@respx.mock
def test_iterate_max_pages():
    page1 = SAMPLE_FEED
    # second page without next link
    page2 = SAMPLE_FEED.replace(b'rel="next"', b'rel="prev"').replace(
        b"Savornin Lohman", b"Second Person"
    )
    route = respx.get(url__regex=r".*/Feed.*")
    route.side_effect = [
        httpx.Response(200, content=page1),
        httpx.Response(200, content=page2),
    ]
    with SyncFeedClient() as client:
        entries = list(client.iterate(category="Persoon", max_pages=2))
    assert len(entries) == 2
