"""Shared HTTP helpers."""

from __future__ import annotations

from typing import Any

import httpx

from tweedekamer.exceptions import HTTPError, NotFoundError

DEFAULT_ODATA_BASE = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0"
DEFAULT_SYNCFEED_BASE = "https://gegevensmagazijn.tweedekamer.nl/SyncFeed/2.0"
DEFAULT_TIMEOUT = 60.0
PAGE_SIZE = 250


def default_user_agent(version: str) -> str:
    return f"tweedekamer-python/{version} (+https://opendata.tweedekamer.nl)"


def raise_for_status(response: httpx.Response) -> None:
    """Map HTTP failures to library exceptions."""
    if response.is_success:
        return

    body = response.text
    if len(body) > 500:
        body = body[:500] + "…"

    message = f"HTTP {response.status_code} for {response.request.method} {response.url}"
    if response.status_code == 404:
        raise NotFoundError(
            message,
            status_code=response.status_code,
            url=str(response.url),
            body=body,
        )
    raise HTTPError(
        message,
        status_code=response.status_code,
        url=str(response.url),
        body=body,
    )


def ensure_client(
    client: httpx.Client | None,
    *,
    timeout: float,
    headers: dict[str, str],
) -> tuple[httpx.Client, bool]:
    """Return an httpx client and whether the caller owns its lifecycle."""
    if client is not None:
        return client, False
    return httpx.Client(timeout=timeout, headers=headers, follow_redirects=True), True


def parse_json(response: httpx.Response) -> Any:
    raise_for_status(response)
    return response.json()
