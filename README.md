# tweedekamer

Python client for the [Tweede Kamer Open Data Portaal](https://opendata.tweedekamer.nl/documentatie/introductie).

Query parliamentary open data with the **OData** API, or incrementally synchronise it with the **SyncFeed** API. Built for modern Python (3.11+), typed with Pydantic v2, and managed with [uv](https://docs.astral.sh/uv/).

## Install

```bash
# with uv
uv add tweedekamer

# or pip
pip install tweedekamer
```

Local development:

```bash
git clone <repo>
cd tweedekamer_api
uv sync
```

## Quick start

```python
from tweedekamer import Client

with Client() as client:
    # Active Tweede Kamer members
    mps = (
        client.personen.exclude_deleted()
        .filter("FractieZetelPersoon/any(a: a/TotEnMet eq null)")
        .order_by("Achternaam")
        .top(20)
        .all()
    )
    for p in mps:
        print(p.roepnaam, p.achternaam)

    # Recent motions
    moties = (
        client.zaken.exclude_deleted()
        .filter("Soort eq 'Motie'")
        .order_by("GestartOp", desc=True)
        .top(5)
        .all()
    )
```

### SyncFeed

```python
from tweedekamer import SyncFeedClient

with SyncFeedClient() as feed:
    page = feed.fetch(category="Zaak")
    for entry in page.entries:
        print(entry.updated, entry.payload.get("nummer"))
    # continue later with page.skip_token
```

## Features

- Fluent OData query builder (`filter`, `select`, `expand`, `order_by`, `top`, `skip`, `count`)
- Automatic pagination via `iterate()`
- Pydantic models for all **38** entity sets
- Binary resource download (`/resource`)
- SyncFeed Atom client with skiptoken support
- Typed package (`py.typed`) and MkDocs documentation

## Documentation

Build and serve the docs locally:

```bash
uv run mkdocs serve
```

Pages cover [getting started](docs/getting-started.md), [OData](docs/odata.md), [SyncFeed](docs/syncfeed.md), and [entities](docs/entities.md).

Official Tweede Kamer docs:

- [Introductie](https://opendata.tweedekamer.nl/documentatie/introductie)
- [OData API](https://opendata.tweedekamer.nl/documentatie/odata-api)
- [SyncFeed API](https://opendata.tweedekamer.nl/documentatie/syncfeed-api)
- [Informatiemodel](https://opendata.tweedekamer.nl/documentatie/informatiemodel)

## Examples

```bash
uv run python examples/list_active_mps.py
uv run python examples/search_moties.py
uv run python examples/sync_feed_sample.py
```

## Development

```bash
uv sync
uv run pytest
uv run ruff check src tests
uv run mkdocs build
```

Live integration tests (optional):

```bash
TWEEDEKAMER_LIVE=1 uv run pytest -m integration
```

## Disclaimer

This library is an independent client for public open data. Usage of the Tweede Kamer APIs is subject to the [Open Data Portaal disclaimer](https://opendata.tweedekamer.nl/disclaimer). No API key is required.

## License

MIT — see [LICENSE](LICENSE).
