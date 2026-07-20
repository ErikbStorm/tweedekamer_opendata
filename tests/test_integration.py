"""Optional live-API integration tests.

Run with::

    uv run pytest -m integration
"""

from __future__ import annotations

import os

import pytest

from tweedekamer import Client, SyncFeedClient

pytestmark = pytest.mark.integration

skip_live = pytest.mark.skipif(
    os.environ.get("TWEEDEKAMER_LIVE") != "1",
    reason="Set TWEEDEKAMER_LIVE=1 to run live integration tests",
)


@skip_live
def test_live_personen():
    with Client() as client:
        people = client.personen.exclude_deleted().top(3).all()
    assert len(people) == 3
    assert people[0].id is not None


@skip_live
def test_live_syncfeed():
    with SyncFeedClient() as feed:
        page = feed.fetch(category="Fractie")
    assert page.entries
    assert page.skip_token or page.next_link
