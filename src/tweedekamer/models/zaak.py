"""Domain models for zaak entities."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field

from tweedekamer.models.base import EntityBase

if TYPE_CHECKING:
    from tweedekamer.models.activiteit import Activiteit  # noqa: F401
    from tweedekamer.models.activiteit import Agendapunt  # noqa: F401
    from tweedekamer.models.activiteit import Besluit  # noqa: F401
    from tweedekamer.models.commissie import Commissie  # noqa: F401
    from tweedekamer.models.document import Document  # noqa: F401
    from tweedekamer.models.fractie import Fractie  # noqa: F401
    from tweedekamer.models.document import Kamerstukdossier  # noqa: F401
    from tweedekamer.models.persoon import Persoon  # noqa: F401


class Zaak(EntityBase):
    """OData entity type ``Zaak``."""

    id: UUID = Field(alias="Id")
    nummer: str | None = Field(default=None, alias="Nummer")
    soort: str | None = Field(default=None, alias="Soort")
    titel: str | None = Field(default=None, alias="Titel")
    citeertitel: str | None = Field(default=None, alias="Citeertitel")
    alias: str | None = Field(default=None, alias="Alias")
    status: str | None = Field(default=None, alias="Status")
    onderwerp: str | None = Field(default=None, alias="Onderwerp")
    gestart_op: datetime | None = Field(default=None, alias="GestartOp")
    organisatie: str | None = Field(default=None, alias="Organisatie")
    grondslagvoorhang: str | None = Field(default=None, alias="Grondslagvoorhang")
    termijn: datetime | None = Field(default=None, alias="Termijn")
    vergaderjaar: str | None = Field(default=None, alias="Vergaderjaar")
    volgnummer: int | None = Field(default=None, alias="Volgnummer")
    huidige_behandelstatus: str | None = Field(default=None, alias="HuidigeBehandelstatus")
    afgedaan: bool | None = Field(default=None, alias="Afgedaan")
    groot_project: bool | None = Field(default=None, alias="GrootProject")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    kabinetsappreciatie: str | None = Field(default=None, alias="Kabinetsappreciatie")
    zaak_actor: list[ZaakActor] | None = Field(default=None, alias="ZaakActor")
    activiteit: list[Activiteit] | None = Field(default=None, alias="Activiteit")
    agendapunt: list[Agendapunt] | None = Field(default=None, alias="Agendapunt")
    besluit: list[Besluit] | None = Field(default=None, alias="Besluit")
    document: list[Document] | None = Field(default=None, alias="Document")
    kamerstukdossier: list[Kamerstukdossier] | None = Field(default=None, alias="Kamerstukdossier")
    vervangen_door: list[Zaak] | None = Field(default=None, alias="VervangenDoor")
    gerelateerd_naar: list[Zaak] | None = Field(default=None, alias="GerelateerdNaar")
    gerelateerd_vanuit: list[Zaak] | None = Field(default=None, alias="GerelateerdVanuit")
    vervangen_vanuit: list[Zaak] | None = Field(default=None, alias="VervangenVanuit")


class ZaakActor(EntityBase):
    """OData entity type ``ZaakActor``."""

    id: UUID = Field(alias="Id")
    zaak__id: UUID | None = Field(default=None, alias="Zaak_Id")
    actor_naam: str | None = Field(default=None, alias="ActorNaam")
    actor_fractie: str | None = Field(default=None, alias="ActorFractie")
    actor_afkorting: str | None = Field(default=None, alias="ActorAfkorting")
    functie: str | None = Field(default=None, alias="Functie")
    relatie: str | None = Field(default=None, alias="Relatie")
    sid_actor: str | None = Field(default=None, alias="SidActor")
    persoon__id: UUID | None = Field(default=None, alias="Persoon_Id")
    fractie__id: UUID | None = Field(default=None, alias="Fractie_Id")
    commissie__id: UUID | None = Field(default=None, alias="Commissie_Id")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    commissie: Commissie | None = Field(default=None, alias="Commissie")
    fractie: Fractie | None = Field(default=None, alias="Fractie")
    persoon: Persoon | None = Field(default=None, alias="Persoon")
    zaak: Zaak | None = Field(default=None, alias="Zaak")


class Toezegging(EntityBase):
    """OData entity type ``Toezegging``."""

    id: UUID = Field(alias="Id")
    aanmaakdatum: datetime | None = Field(default=None, alias="Aanmaakdatum")
    nummer: str | None = Field(default=None, alias="Nummer")
    activiteit_nummer: str | None = Field(default=None, alias="ActiviteitNummer")
    naam: str | None = Field(default=None, alias="Naam")
    achternaam: str | None = Field(default=None, alias="Achternaam")
    initialen: str | None = Field(default=None, alias="Initialen")
    voornaam: str | None = Field(default=None, alias="Voornaam")
    achtervoegsel: str | None = Field(default=None, alias="Achtervoegsel")
    titulatuur: str | None = Field(default=None, alias="Titulatuur")
    functie: str | None = Field(default=None, alias="Functie")
    status: str | None = Field(default=None, alias="Status")
    datum_nakoming: datetime | None = Field(default=None, alias="DatumNakoming")
    ministerie: str | None = Field(default=None, alias="Ministerie")
    tekst: str | None = Field(default=None, alias="Tekst")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    tussenvoegsel: str | None = Field(default=None, alias="Tussenvoegsel")
    notities: str | None = Field(default=None, alias="Notities")
    activiteit: list[Activiteit] | None = Field(default=None, alias="Activiteit")
    kamerbrief_nakoming: list[Document] | None = Field(default=None, alias="KamerbriefNakoming")
    toegezegd_aan: list[ToegezegdAan] | None = Field(default=None, alias="ToegezegdAan")
    is_herhaling_van: list[Toezegging] | None = Field(default=None, alias="IsHerhalingVan")
    is_wijziging_van: list[Toezegging] | None = Field(default=None, alias="IsWijzigingVan")
    is_aanvulling_op: list[Toezegging] | None = Field(default=None, alias="IsAanvullingOp")
    is_aangevuld_vanuit: list[Toezegging] | None = Field(default=None, alias="IsAangevuldVanuit")
    is_herhaald_door: list[Toezegging] | None = Field(default=None, alias="IsHerhaaldDoor")
    is_gewijzigd_door: list[Toezegging] | None = Field(default=None, alias="IsGewijzigdDoor")


class ToegezegdAan(EntityBase):
    """OData entity type ``ToegezegdAan``."""

    toezegging__id: UUID | None = Field(default=None, alias="Toezegging_Id")
    fractie__id: UUID | None = Field(default=None, alias="Fractie_Id")
    persoon__id: UUID | None = Field(default=None, alias="Persoon_Id")
    toezegging: Toezegging | None = Field(default=None, alias="Toezegging")
    fractie: Fractie | None = Field(default=None, alias="Fractie")
    persoon: Persoon | None = Field(default=None, alias="Persoon")
