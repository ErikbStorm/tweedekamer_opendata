# OData API

Base URL (v4 / data 2.0):

```text
https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0
```

Official documentation: [OData API](https://opendata.tweedekamer.nl/documentatie/odata-api).

## Entity-set accessors

Typed accessors mirror the OData entity sets:

```python
client.personen
client.zaken
client.documenten
client.fracties
client.commissies
client.stemmingen
client.activiteiten
# … see Entities page for the full list
```

Generic access (any set name):

```python
client.entity("Reservering").top(10).all()
```

## Building a query

`ODataQuery` methods return new query objects (chain freely):

| Method | OData option |
| --- | --- |
| `filter(expr)` | `$filter` |
| `filter_eq(field, value)` | `$filter` with typed value |
| `exclude_deleted()` | `Verwijderd eq false` |
| `select(*fields)` | `$select` |
| `expand(*navs)` | `$expand` |
| `order_by(field, desc=False)` | `$orderby` |
| `top(n)` | `$top` |
| `skip(n)` | `$skip` |
| `count()` | `$count=true` |
| `all()` | execute one page |
| `first()` | first match or `None` |
| `iterate(max_items=…)` | auto-pagination |
| `get(id)` | single entity |
| `download_resource(id)` | `…/resource` |

### Filters

Raw OData expressions:

```python
client.personen.filter(
    "Verwijderd eq false and (Functie eq 'Tweede Kamerlid' or Functie eq 'Eerste Kamerlid')"
)
```

Helpers:

```python
client.personen.filter_eq("Functie", "Tweede Kamerlid")
client.personen.filter_ne("Verwijderd", True)
```

String values with quotes are escaped (`O'Reilly` → `'O''Reilly'`).

### Expand related entities

```python
client.zaken.filter("Soort eq 'Motie'").expand(
    "ZaakActor($filter=Relatie eq 'Indiener')"
).top(10).all()
```

Nested expand options use OData’s `(…)` syntax; separate multiple expand options with `;` inside the fragment when needed.

### Pagination

The service returns at most **250** entities per response.

- `all()` — single request (respects your `top()` / default page)
- `iterate()` — follows `@odata.nextLink` when present, otherwise advances with `$skip`

```python
for doc in client.documenten.exclude_deleted().iterate(max_items=1000):
    process(doc)
```

### Count

```python
total = client.zaken.exclude_deleted().filter("Soort eq 'Motie'").count()
```

### Metadata level

Defaults to `odata.metadata=none` for smaller payloads. Override at client construction:

```python
Client(metadata_level="full")
```

## Resources

When an entity has a binary attachment (portrait photo, document file, …):

```python
bytes_ = client.documenten.download_resource(document_id)
client.personen.download_resource(person_id, path="photo.jpg")
```

Equivalent OData path: `/{EntitySet}({id})/resource`.

## Errors

| Exception | When |
| --- | --- |
| `NotFoundError` | HTTP 404 |
| `HTTPError` | Other non-success HTTP statuses |
| `QueryError` | Invalid local query construction |
| `TweedekamerError` | Base class |

## Service document

```python
client.entity_sets()  # list of entity set names from the service root
```
