"""Fluent OData query builder."""

from __future__ import annotations

from collections.abc import Iterator
from typing import TYPE_CHECKING, Any, Generic, TypeVar
from urllib.parse import quote
from uuid import UUID

from tweedekamer._http import PAGE_SIZE, parse_json, raise_for_status
from tweedekamer.exceptions import NotFoundError, QueryError
from tweedekamer.models.base import EntityBase

if TYPE_CHECKING:
    import httpx

T = TypeVar("T", bound=EntityBase)


def _format_odata_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, UUID):
        return str(value)
    # string — escape single quotes per OData
    text = str(value).replace("'", "''")
    return f"'{text}'"


class ODataQuery(Generic[T]):
    """Build and execute an OData query against a single entity set."""

    def __init__(
        self,
        *,
        http: httpx.Client,
        base_url: str,
        entity_set: str,
        model: type[T],
        metadata_level: str = "none",
    ) -> None:
        self._http = http
        self._base_url = base_url.rstrip("/")
        self._entity_set = entity_set
        self._model = model
        self._metadata_level = metadata_level

        self._filters: list[str] = []
        self._select: list[str] | None = None
        self._expand: list[str] | None = None
        self._orderby: list[str] = []
        self._top: int | None = None
        self._skip: int | None = None
        self._count: bool = False

    # -- immutable-style cloning -------------------------------------------

    def _clone(self) -> ODataQuery[T]:
        q = ODataQuery(
            http=self._http,
            base_url=self._base_url,
            entity_set=self._entity_set,
            model=self._model,
            metadata_level=self._metadata_level,
        )
        q._filters = list(self._filters)
        q._select = list(self._select) if self._select is not None else None
        q._expand = list(self._expand) if self._expand is not None else None
        q._orderby = list(self._orderby)
        q._top = self._top
        q._skip = self._skip
        q._count = self._count
        return q

    # -- query options -----------------------------------------------------

    def filter(self, expression: str) -> ODataQuery[T]:
        """Add a raw OData ``$filter`` expression (combined with ``and``)."""
        expression = expression.strip()
        if not expression:
            raise QueryError("Filter expression must not be empty")
        q = self._clone()
        q._filters.append(expression)
        return q

    def filter_eq(self, field: str, value: Any) -> ODataQuery[T]:
        """Filter where ``field eq value``."""
        return self.filter(f"{field} eq {_format_odata_value(value)}")

    def filter_ne(self, field: str, value: Any) -> ODataQuery[T]:
        return self.filter(f"{field} ne {_format_odata_value(value)}")

    def exclude_deleted(self) -> ODataQuery[T]:
        """Exclude soft-deleted entities (``Verwijderd eq false``)."""
        return self.filter("Verwijderd eq false")

    def select(self, *fields: str) -> ODataQuery[T]:
        """Limit returned attributes with ``$select``."""
        if not fields:
            raise QueryError("select() requires at least one field")
        q = self._clone()
        q._select = list(fields)
        return q

    def expand(self, *navigations: str) -> ODataQuery[T]:
        """Include related entities with ``$expand``.

        Nested options are supported as raw fragments, e.g.
        ``expand("ZaakActor($filter=Relatie eq 'Indiener')")``.
        """
        if not navigations:
            raise QueryError("expand() requires at least one navigation property")
        q = self._clone()
        q._expand = list(navigations)
        return q

    def order_by(self, field: str, *, desc: bool = False) -> ODataQuery[T]:
        """Sort results with ``$orderby``."""
        q = self._clone()
        q._orderby.append(f"{field} desc" if desc else field)
        return q

    def top(self, n: int) -> ODataQuery[T]:
        if n < 0:
            raise QueryError("top() must be >= 0")
        q = self._clone()
        q._top = n
        return q

    def skip(self, n: int) -> ODataQuery[T]:
        if n < 0:
            raise QueryError("skip() must be >= 0")
        q = self._clone()
        q._skip = n
        return q

    # -- URL construction --------------------------------------------------

    def _query_params(self, *, include_count: bool = False) -> dict[str, str]:
        params: dict[str, str] = {
            "$format": f"application/json;odata.metadata={self._metadata_level}",
        }
        if self._filters:
            if len(self._filters) == 1:
                params["$filter"] = self._filters[0]
            else:
                params["$filter"] = " and ".join(f"({f})" for f in self._filters)
        if self._select:
            params["$select"] = ",".join(self._select)
        if self._expand:
            params["$expand"] = ",".join(self._expand)
        if self._orderby:
            params["$orderby"] = ",".join(self._orderby)
        if self._top is not None:
            params["$top"] = str(self._top)
        if self._skip is not None:
            params["$skip"] = str(self._skip)
        if include_count or self._count:
            params["$count"] = "true"
        return params

    def build_url(self, *, entity_id: UUID | str | None = None, resource: bool = False) -> str:
        """Return the absolute URL for this query (without query string for path-only)."""
        path = f"{self._base_url}/{self._entity_set}"
        if entity_id is not None:
            path = f"{path}({entity_id})"
        if resource:
            path = f"{path}/resource"
        return path

    # -- execution ---------------------------------------------------------

    def _parse_entity(self, raw: dict[str, Any]) -> T:
        return self._model.model_validate(raw)

    def _get_json(self, url: str, params: dict[str, str] | None = None) -> Any:
        response = self._http.get(url, params=params)
        return parse_json(response)

    def all(self) -> list[T]:
        """Execute the query and return a single page of results (max 250)."""
        url = self.build_url()
        data = self._get_json(url, self._query_params())
        values = data.get("value", [])
        return [self._parse_entity(item) for item in values]

    def first(self) -> T | None:
        """Return the first matching entity, or ``None``."""
        items = self.top(1).all()
        return items[0] if items else None

    def count(self) -> int:
        """Return the total number of matching entities (``$count=true``)."""
        q = self._clone()
        q._top = 0
        q._skip = None
        url = q.build_url()
        data = self._get_json(url, q._query_params(include_count=True))
        if "@odata.count" not in data:
            # fallback: some servers use odata.count
            if "odata.count" in data:
                return int(data["odata.count"])
            raise QueryError("Response did not include @odata.count", details=data)
        return int(data["@odata.count"])

    def iterate(self, *, max_items: int | None = None) -> Iterator[T]:
        """Yield entities across pages (follows ``@odata.nextLink`` or uses ``$skip``).

        Args:
            max_items: Stop after this many entities. ``None`` means no limit.
        """
        yielded = 0
        # Prefer nextLink when present; otherwise page with $skip
        q = self._clone()
        if q._top is None:
            # fetch full pages unless user set top as overall limit via max_items
            page_size = PAGE_SIZE
        else:
            page_size = min(q._top, PAGE_SIZE)

        # If user set top without iterate semantics, honour as overall max
        overall_max = max_items
        if q._top is not None and (overall_max is None or q._top < overall_max):
            overall_max = q._top

        skip = q._skip or 0
        next_url: str | None = None
        next_params: dict[str, str] | None = None

        # First request
        first = q._clone()
        first._skip = skip
        if overall_max is not None:
            first._top = min(page_size, overall_max)
        else:
            first._top = page_size
        next_url = first.build_url()
        next_params = first._query_params()

        while next_url:
            data = self._get_json(next_url, next_params)
            values = data.get("value", [])
            for item in values:
                yield self._parse_entity(item)
                yielded += 1
                if overall_max is not None and yielded >= overall_max:
                    return

            next_link = data.get("@odata.nextLink") or data.get("odata.nextLink")
            if next_link:
                next_url = next_link
                next_params = None  # nextLink is complete
                continue

            # Manual pagination when nextLink is absent but page was full
            if len(values) < (first._top or page_size):
                return
            if overall_max is not None and yielded >= overall_max:
                return

            skip += len(values)
            remaining = None if overall_max is None else overall_max - yielded
            page = q._clone()
            page._skip = skip
            page._top = page_size if remaining is None else min(page_size, remaining)
            next_url = page.build_url()
            next_params = page._query_params()

    def get(self, entity_id: UUID | str, *, expand: list[str] | None = None) -> T:
        """Fetch a single entity by id."""
        q = self._clone()
        if expand:
            q = q.expand(*expand)
        url = q.build_url(entity_id=entity_id)
        params = q._query_params()
        # $filter/$skip/$top don't apply to single-entity GETs
        for key in ("$filter", "$skip", "$top", "$orderby", "$count"):
            params.pop(key, None)
        try:
            data = self._get_json(url, params)
        except NotFoundError:
            raise
        # Single entity responses are the object itself (not wrapped in value)
        if isinstance(data, dict) and "value" in data and "Id" not in data and "id" not in data:
            # unexpected collection
            values = data["value"]
            if not values:
                raise NotFoundError(
                    f"{self._entity_set}({entity_id}) not found",
                    status_code=404,
                    url=url,
                )
            data = values[0]
        return self._parse_entity(data)

    def download_resource(
        self,
        entity_id: UUID | str,
        *,
        path: str | None = None,
    ) -> bytes:
        """Download the binary resource attached to an entity.

        Args:
            entity_id: Entity id (GUID).
            path: If set, write the bytes to this filesystem path.

        Returns:
            Raw file bytes.
        """
        url = self.build_url(entity_id=entity_id, resource=True)
        response = self._http.get(url)
        raise_for_status(response)
        content = response.content
        if path is not None:
            with open(path, "wb") as fh:
                fh.write(content)
        return content

    def __repr__(self) -> str:
        params = self._query_params()
        safe = "'()/"
        qs = "&".join(f"{k}={quote(v, safe=safe)}" for k, v in params.items())
        return f"ODataQuery({self._entity_set}?{qs})"
