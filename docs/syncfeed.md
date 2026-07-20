# SyncFeed API

Base URL (2.0):

```text
https://gegevensmagazijn.tweedekamer.nl/SyncFeed/2.0
```

Official documentation: [SyncFeed API](https://opendata.tweedekamer.nl/documentatie/syncfeed-api).

Use SyncFeed when you want to **synchronise** (part of) the Gegevensmagazijn into your own database. The feed is Atom 1.0 XML and supports continuation via `skiptoken`.

## Fetch a page

```python
from tweedekamer import SyncFeedClient

with SyncFeedClient() as feed:
    page = feed.fetch(category="Zaak")
    print(page.title, len(page.entries))
    print("continue with", page.skip_token)
```

### Parameters

| Argument | Meaning |
| --- | --- |
| `category` | Limit to one entity kind (e.g. `Persoon`, `Zaak`, `Document`) |
| `skiptoken` | Continuation token from a previous `FeedPage.skip_token` |

## Entries

Each `FeedEntry` exposes:

- `id` — Atom entry id (URL)
- `category` — entity kind term
- `updated` — last change timestamp
- `payload` — parsed XML body as a nested `dict`
- `raw_xml` — original content XML (when present)
- `entity_id` — best-effort UUID

```python
for entry in page.entries:
    print(entry.updated, entry.category, entry.payload.get("nummer"))
```

## Walking the full feed

```python
token = None
while True:
    page = feed.fetch(category="Document", skiptoken=token)
    for entry in page.entries:
        upsert(entry)
    if not page.skip_token:
        break
    token = page.skip_token
```

Or:

```python
for entry in feed.iterate(category="Document", max_pages=10):
    upsert(entry)
```

## Single entity / resource

```python
xml_bytes = feed.get_entity(entity_id)
data = feed.get_entity_parsed(entity_id)
file_bytes = feed.download_resource(entity_id, path="file.bin")
```

Endpoints used:

- `GET /Feed`
- `GET /Entiteiten/{id}`
- `GET /Resources/{id}`

## OData vs SyncFeed

| | OData | SyncFeed |
| --- | --- | --- |
| Format | JSON | Atom/XML |
| Best for | Ad-hoc search | Continuous sync |
| Filtering | Rich `$filter` | Category + time order via feed |
| Client | `Client` | `SyncFeedClient` |
