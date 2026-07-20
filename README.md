# tweedekamer_opendata

Python client for the [Tweede Kamer Open Data Portaal](https://opendata.tweedekamer.nl/documentatie/introductie).

Query parliamentary open data with the **OData** API, or incrementally synchronise it with the **SyncFeed** API. Built for modern Python (3.11+), typed with Pydantic v2, and managed with [uv](https://docs.astral.sh/uv/).

**PyPI name:** `tweedekamer_opendata` · **Import:** `tweedekamer`

## Install

```bash
# with uv
uv add tweedekamer_opendata

# or pip
pip install tweedekamer_opendata
```

Local development:

```bash
git clone https://github.com/ErikbStorm/tweedekamer_opendata.git
cd tweedekamer_opendata
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
uv run pre-commit install   # ruff + pytest on every commit
uv run pytest
uv run ruff check src tests
uv run mkdocs build
```

### Pre-commit hooks

Hooks run **Ruff** (lint + format) and **pytest** before each commit:

```bash
uv run pre-commit install
uv run pre-commit run --all-files   # run manually
```

Skip once if needed: `SKIP=pytest git commit ...` or `git commit --no-verify`.

Live integration tests (optional):

```bash
TWEEDEKAMER_LIVE=1 uv run pytest -m integration
```

### Publishing to PyPI

Releases use GitHub Actions with [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OIDC) — no API token in the repo.

**One-time setup**

1. On GitHub: **Settings → Environments → New environment** named `pypi`.
2. On [PyPI](https://pypi.org/manage/account/publishing/): add a trusted publisher:
   - **Owner:** `ErikbStorm`
   - **Repository:** `tweedekamer_opendata`
   - **Workflow:** `publish.yml`
   - **Environment:** `pypi`
3. (First release only) If the project does not exist on PyPI yet, use a **pending publisher** with the same fields.

**Release a new version**

1. Bump `version` in `pyproject.toml` and `src/tweedekamer/_version.py`.
2. Commit, push, and create a GitHub Release (e.g. tag `v0.1.0`).
3. Publishing the release runs [`.github/workflows/publish.yml`](.github/workflows/publish.yml): tests → `uv build` → `uv publish` as **`tweedekamer_opendata`**.

You can also run the workflow manually (**Actions → Publish to PyPI → Run workflow**) and type `publish` to confirm.

Package page (after first release): https://pypi.org/project/tweedekamer_opendata/

## Disclaimer

This library is an independent client for public open data. Usage of the Tweede Kamer APIs is subject to the [Open Data Portaal disclaimer](https://opendata.tweedekamer.nl/disclaimer). No API key is required.

## License

MIT — see [LICENSE](LICENSE).
