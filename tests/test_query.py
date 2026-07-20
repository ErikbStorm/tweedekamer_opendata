"""Unit tests for the OData client and query builder."""

from __future__ import annotations

import re
from uuid import UUID

import httpx
import pytest
import respx

from tweedekamer import Client, NotFoundError, QueryError
from tweedekamer.models import Persoon

PERSON_ID = "e55ca731-e1aa-44c0-a5f3-0008c23976f7"
ODATA = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0"


def _person_payload(**overrides):
    data = {
        "Id": PERSON_ID,
        "Nummer": 1034,
        "Roepnaam": "Joop",
        "Achternaam": "Atsma",
        "Functie": "Eerste Kamerlid",
        "Verwijderd": False,
        "Fractielabel": "CDA",
    }
    data.update(overrides)
    return data


@respx.mock
def test_list_personen():
    route = respx.get(f"{ODATA}/Persoon").mock(
        return_value=httpx.Response(200, json={"value": [_person_payload()]})
    )
    with Client() as client:
        people = client.personen.exclude_deleted().top(1).all()
    assert route.called
    assert len(people) == 1
    assert isinstance(people[0], Persoon)
    assert people[0].roepnaam == "Joop"
    assert people[0].achternaam == "Atsma"
    params = route.calls.last.request.url.params
    assert params["$filter"] == "Verwijderd eq false"
    assert params["$top"] == "1"


@respx.mock
def test_filter_eq_and_select():
    respx.get(f"{ODATA}/Persoon").mock(
        return_value=httpx.Response(200, json={"value": [_person_payload()]})
    )
    with Client() as client:
        people = (
            client.personen.filter_eq("Functie", "Tweede Kamerlid")
            .select("Id", "Roepnaam", "Achternaam")
            .all()
        )
    assert people[0].id == UUID(PERSON_ID)
    req = respx.calls.last.request
    assert "Functie eq 'Tweede Kamerlid'" in req.url.params["$filter"]
    assert req.url.params["$select"] == "Id,Roepnaam,Achternaam"


@respx.mock
def test_get_by_id():
    respx.get(url__regex=rf".*/Persoon\({PERSON_ID}\)").mock(
        return_value=httpx.Response(200, json=_person_payload())
    )
    with Client() as client:
        person = client.personen.get(PERSON_ID)
    assert person.achternaam == "Atsma"


@respx.mock
def test_get_not_found():
    respx.get(url__regex=r".*/Persoon\(.+\)").mock(
        return_value=httpx.Response(404, text="not found")
    )
    with Client() as client:
        with pytest.raises(NotFoundError):
            client.personen.get(PERSON_ID)


@respx.mock
def test_count():
    respx.get(f"{ODATA}/Zaak").mock(
        return_value=httpx.Response(200, json={"@odata.count": 42, "value": []})
    )
    with Client() as client:
        n = client.zaken.filter("Soort eq 'Motie'").count()
    assert n == 42
    params = respx.calls.last.request.url.params
    assert params["$count"] == "true"
    assert params["$top"] == "0"


@respx.mock
def test_iterate_with_next_link():
    page1 = {
        "value": [_person_payload(Id="00000000-0000-0000-0000-000000000001", Achternaam="A")],
        "@odata.nextLink": f"{ODATA}/Persoon?$skiptoken=page2",
    }
    page2 = {
        "value": [_person_payload(Id="00000000-0000-0000-0000-000000000002", Achternaam="B")],
    }
    route = respx.get(url__regex=rf"{re.escape(ODATA)}/Persoon.*")
    route.side_effect = [
        httpx.Response(200, json=page1),
        httpx.Response(200, json=page2),
    ]

    with Client() as client:
        names = [p.achternaam for p in client.personen.iterate(max_items=10)]
    assert names == ["A", "B"]
    assert route.call_count == 2


@respx.mock
def test_download_resource(tmp_path):
    content = b"\xff\xd8\xff fake jpeg"
    respx.get(url__regex=rf".*/Persoon\({PERSON_ID}\)/resource").mock(
        return_value=httpx.Response(200, content=content)
    )
    path = tmp_path / "photo.jpg"
    with Client() as client:
        data = client.personen.download_resource(PERSON_ID, path=str(path))
    assert data == content
    assert path.read_bytes() == content


@respx.mock
def test_entity_sets():
    respx.get(ODATA).mock(
        return_value=httpx.Response(
            200,
            json={
                "value": [
                    {"name": "Persoon", "kind": "EntitySet", "url": "Persoon"},
                    {"name": "Something", "kind": "Singleton", "url": "Something"},
                ]
            },
        )
    )
    with Client() as client:
        sets = client.entity_sets()
    assert sets == ["Persoon"]


def test_empty_filter_raises():
    with Client() as client:
        with pytest.raises(QueryError):
            client.personen.filter("  ")


def test_filter_eq_string_escape():
    with Client() as client:
        q = client.personen.filter_eq("Titel", "O'Reilly")
        params = q._query_params()
    assert params["$filter"] == "Titel eq 'O''Reilly'"


@respx.mock
def test_expand_and_order_by():
    respx.get(f"{ODATA}/Zaak").mock(return_value=httpx.Response(200, json={"value": []}))
    with Client() as client:
        client.zaken.expand("ZaakActor").order_by("GestartOp", desc=True).top(5).all()
    params = respx.calls.last.request.url.params
    assert params["$expand"] == "ZaakActor"
    assert params["$orderby"] == "GestartOp desc"


@respx.mock
def test_generic_entity():
    respx.get(f"{ODATA}/Reservering").mock(
        return_value=httpx.Response(
            200,
            json={
                "value": [
                    {
                        "Id": "11111111-1111-1111-1111-111111111111",
                        "Verwijderd": False,
                    }
                ]
            },
        )
    )
    with Client() as client:
        rows = client.entity("Reservering").top(1).all()
    assert rows[0].id == UUID("11111111-1111-1111-1111-111111111111")
