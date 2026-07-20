# Getting started

## Requirements

- Python 3.11+
- Network access to `gegevensmagazijn.tweedekamer.nl`

## Create a client

```python
from tweedekamer import Client

client = Client()
# ... use client ...
client.close()
```

Or as a context manager (preferred):

```python
from tweedekamer import Client

with Client() as client:
    people = client.personen.top(5).all()
```

### Options

```python
Client(
    base_url="https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0",
    timeout=60.0,
    user_agent="my-app/1.0",
    metadata_level="none",  # none | minimal | full
)
```

## Soft-deleted entities

The Gegevensmagazijn keeps deleted rows as placeholders so history can be reconstructed. Official docs recommend filtering them out for normal use:

```python
client.personen.exclude_deleted()  # adds: Verwijderd eq false
```

## First queries

### Active MPs

```python
mps = (
    client.personen.exclude_deleted()
    .filter("FractieZetelPersoon/any(a: a/TotEnMet eq null)")
    .select("Roepnaam", "Achternaam", "Functie")
    .order_by("Achternaam")
    .all()
)
```

### Motions (moties)

```python
moties = (
    client.zaken.exclude_deleted()
    .filter("Soort eq 'Motie'")
    .order_by("GestartOp", desc=True)
    .top(25)
    .all()
)
```

### Count matches

```python
n = client.zaken.exclude_deleted().filter("Soort eq 'Motie'").count()
print(n)
```

### Fetch one entity + related data

```python
from uuid import UUID

zaak = client.zaken.get(
    UUID("…"),
    expand=["ZaakActor($filter=Relatie eq 'Indiener')"],
)
```

### Download a file (portrait, PDF, …)

```python
client.personen.download_resource(person_id, path="portrait.jpg")
# or: raw_bytes = client.personen.download_resource(person_id)
```

## Field naming

API responses use PascalCase (`Achternaam`). Models expose **snake_case** attributes (`achternaam`) while still accepting the original names when validating JSON.

```python
person.achternaam
person.get("Achternaam")  # also works
```

## Next steps

- [OData guide](odata.md) — filters, expand, pagination
- [SyncFeed guide](syncfeed.md) — incremental sync
- [Entities](entities.md) — all 38 entity sets
