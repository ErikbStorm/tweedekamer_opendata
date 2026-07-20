"""Shared pytest fixtures."""

from __future__ import annotations

import httpx
import pytest

from tweedekamer import Client, SyncFeedClient

ODATA_BASE = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0"
SYNCFEED_BASE = "https://gegevensmagazijn.tweedekamer.nl/SyncFeed/2.0"


@pytest.fixture
def odata_base() -> str:
    return ODATA_BASE


@pytest.fixture
def syncfeed_base() -> str:
    return SYNCFEED_BASE


@pytest.fixture
def http_client() -> httpx.Client:
    return httpx.Client(timeout=30.0)


@pytest.fixture
def client(http_client: httpx.Client, odata_base: str) -> Client:
    return Client(base_url=odata_base, http_client=http_client)


@pytest.fixture
def sync_client(http_client: httpx.Client, syncfeed_base: str) -> SyncFeedClient:
    return SyncFeedClient(base_url=syncfeed_base, http_client=http_client)
