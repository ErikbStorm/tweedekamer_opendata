"""Security hardening: UUID validation, URL allowlisting, safe XML."""

from __future__ import annotations

import re

import httpx
import pytest
import respx

from tweedekamer import Client, SecurityError, SyncFeedClient
from tweedekamer._security import assert_url_allowed, parse_xml, require_entity_id
from tweedekamer.syncfeed import parse_feed

ODATA = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0"
PERSON_ID = "e55ca731-e1aa-44c0-a5f3-0008c23976f7"


def test_require_entity_id_accepts_uuid():
    assert require_entity_id(PERSON_ID) == PERSON_ID
    assert require_entity_id("E55CA731-E1AA-44C0-A5F3-0008C23976F7") == PERSON_ID


def test_require_entity_id_rejects_path_injection():
    with pytest.raises(SecurityError, match="UUID"):
        require_entity_id("../evil")
    with pytest.raises(SecurityError, match="UUID"):
        require_entity_id("not-a-uuid")
    with pytest.raises(SecurityError, match="UUID"):
        require_entity_id(f"{PERSON_ID})/resource?x=")


def test_assert_url_allowed_same_host():
    url = assert_url_allowed(
        f"{ODATA}/Persoon?$skip=1",
        allowed_base=ODATA,
        purpose="test",
    )
    assert url.startswith(ODATA)


def test_assert_url_allowed_rejects_foreign_host():
    with pytest.raises(SecurityError, match="Refusing"):
        assert_url_allowed(
            "https://evil.example/steal",
            allowed_base=ODATA,
            purpose="OData @odata.nextLink",
        )


def test_assert_url_allowed_resolves_relative():
    url = assert_url_allowed(
        "/OData/v4/2.0/Persoon?$skip=10",
        allowed_base=ODATA,
        purpose="test",
    )
    assert "gegevensmagazijn.tweedekamer.nl" in url


def test_parse_xml_rejects_external_entity_content():
    payload = b"""<?xml version="1.0"?>
    <!DOCTYPE foo [
      <!ENTITY xxe SYSTEM "file:///etc/passwd">
    ]>
    <root>&xxe;</root>
    """
    try:
        root = parse_xml(payload)
        text = "".join(root.itertext())
        assert "root:" not in text
    except SecurityError:
        pass


def test_parse_xml_accepts_normal_document():
    xml = b'<?xml version="1.0"?><root><child>ok</child></root>'
    root = parse_xml(xml)
    assert root.tag == "root"


@respx.mock
def test_odata_get_rejects_bad_entity_id():
    with Client() as client:
        with pytest.raises(SecurityError):
            client.personen.get("../not-uuid")


@respx.mock
def test_odata_iterate_rejects_evil_next_link():
    page1 = {
        "value": [
            {
                "Id": PERSON_ID,
                "Achternaam": "A",
                "Verwijderd": False,
            }
        ],
        "@odata.nextLink": "https://evil.example/exfil",
    }
    respx.get(url__regex=rf"{re.escape(ODATA)}/Persoon.*").mock(
        return_value=httpx.Response(200, json=page1)
    )
    with Client() as client:
        with pytest.raises(SecurityError, match="nextLink"):
            list(client.personen.iterate(max_items=10))


@respx.mock
def test_odata_iterate_allows_same_host_next_link():
    page1 = {
        "value": [
            {
                "Id": "00000000-0000-0000-0000-000000000001",
                "Achternaam": "A",
                "Verwijderd": False,
            }
        ],
        "@odata.nextLink": f"{ODATA}/Persoon?$skiptoken=page2",
    }
    page2 = {
        "value": [
            {
                "Id": "00000000-0000-0000-0000-000000000002",
                "Achternaam": "B",
                "Verwijderd": False,
            }
        ],
    }
    route = respx.get(url__regex=rf"{re.escape(ODATA)}/Persoon.*")
    route.side_effect = [
        httpx.Response(200, json=page1),
        httpx.Response(200, json=page2),
    ]
    with Client() as client:
        names = [p.achternaam for p in client.personen.iterate(max_items=10)]
    assert names == ["A", "B"]


@respx.mock
def test_syncfeed_fetch_url_rejects_evil_host():
    with SyncFeedClient() as client:
        with pytest.raises(SecurityError, match="SyncFeed next link"):
            client.fetch_url("https://evil.example/Feed")


@respx.mock
def test_syncfeed_get_entity_rejects_bad_id():
    with SyncFeedClient() as client:
        with pytest.raises(SecurityError):
            client.get_entity("not-a-uuid")


def test_parse_feed_still_works():
    sample = b"""<?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
      <title>Test</title>
      <updated>2026-07-19T12:00:00Z</updated>
      <link rel="next" href="https://gegevensmagazijn.tweedekamer.nl/SyncFeed/2.0/Feed?skiptoken=1"/>
    </feed>
    """
    page = parse_feed(sample)
    assert page.title == "Test"
    assert page.skip_token == "1"
