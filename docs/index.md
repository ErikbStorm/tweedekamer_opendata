# tweedekamer

Python client for the [Tweede Kamer Open Data Portaal](https://opendata.tweedekamer.nl/documentatie/introductie).

Query parliamentary data (members, motions, documents, votes, committees, …) through the **OData** API, or keep a local copy in sync with the **SyncFeed** API.

## Install

With [uv](https://docs.astral.sh/uv/):

```bash
uv add tweedekamer
```

Or with pip:

```bash
pip install tweedekamer
```

From a local checkout:

```bash
uv sync
```

## 30-second example

```python
from tweedekamer import Client

with Client() as client:
    mps = (
        client.personen.exclude_deleted()
        .filter("FractieZetelPersoon/any(a: a/TotEnMet eq null)")
        .order_by("Achternaam")
        .top(10)
        .all()
    )
    for person in mps:
        print(person.roepnaam, person.achternaam)
```

## What this library covers

| API | Use when | Client |
| --- | --- | --- |
| [OData](odata.md) | Searching / filtering specific data | `Client` |
| [SyncFeed](syncfeed.md) | Incremental sync into your own store | `SyncFeedClient` |

No API key is required. Data is published by the Tweede Kamer; please read the [official disclaimer](https://opendata.tweedekamer.nl/disclaimer).

## Further reading

- [Getting started](getting-started.md)
- [Entity overview](entities.md)
- [API reference](api-reference.md)
- Official docs: [Introductie](https://opendata.tweedekamer.nl/documentatie/introductie) · [OData](https://opendata.tweedekamer.nl/documentatie/odata-api) · [SyncFeed](https://opendata.tweedekamer.nl/documentatie/syncfeed-api) · [Informatiemodel](https://opendata.tweedekamer.nl/documentatie/informatiemodel)
