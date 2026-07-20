"""Python client for the Tweede Kamer Open Data Portaal APIs.

Provides access to the OData search API and the SyncFeed synchronisation API.
See https://opendata.tweedekamer.nl/documentatie/introductie for official docs.
"""

from __future__ import annotations

from tweedekamer._version import __version__
from tweedekamer.client import Client
from tweedekamer.exceptions import (
    HTTPError,
    NotFoundError,
    QueryError,
    TweedekamerError,
)
from tweedekamer.syncfeed import FeedEntry, FeedPage, SyncFeedClient

__all__ = [
    "Client",
    "SyncFeedClient",
    "FeedEntry",
    "FeedPage",
    "TweedekamerError",
    "HTTPError",
    "NotFoundError",
    "QueryError",
    "__version__",
]
