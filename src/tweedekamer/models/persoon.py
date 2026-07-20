"""Domain models for persoon entities."""
from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field

from tweedekamer.models.base import EntityBase

if TYPE_CHECKING:
    from tweedekamer.models.activiteit import ActiviteitActor  # noqa: F401
    from tweedekamer.models.commissie import CommissieZetelVastPersoon  # noqa: F401
    from tweedekamer.models.commissie import CommissieZetelVervangerPersoon  # noqa: F401
    from tweedekamer.models.document import DocumentActor  # noqa: F401
    from tweedekamer.models.fractie import FractieZetelPersoon  # noqa: F401
    from tweedekamer.models.activiteit import Stemming  # noqa: F401
    from tweedekamer.models.zaak import ToegezegdAan  # noqa: F401
    from tweedekamer.models.zaak import ZaakActor  # noqa: F401


class Persoon(EntityBase):
    """OData entity type ``Persoon``."""

    id: UUID = Field(alias="Id")
    nummer: int | None = Field(default=None, alias="Nummer")
    titels: str | None = Field(default=None, alias="Titels")
    initialen: str | None = Field(default=None, alias="Initialen")
    tussenvoegsel: str | None = Field(default=None, alias="Tussenvoegsel")
    achternaam: str | None = Field(default=None, alias="Achternaam")
    voornamen: str | None = Field(default=None, alias="Voornamen")
    roepnaam: str | None = Field(default=None, alias="Roepnaam")
    geslacht: str | None = Field(default=None, alias="Geslacht")
    functie: str | None = Field(default=None, alias="Functie")
    geboortedatum: date | None = Field(default=None, alias="Geboortedatum")
    geboorteplaats: str | None = Field(default=None, alias="Geboorteplaats")
    geboorteland: str | None = Field(default=None, alias="Geboorteland")
    overlijdensdatum: date | None = Field(default=None, alias="Overlijdensdatum")
    overlijdensplaats: str | None = Field(default=None, alias="Overlijdensplaats")
    woonplaats: str | None = Field(default=None, alias="Woonplaats")
    land: str | None = Field(default=None, alias="Land")
    content_type: str | None = Field(default=None, alias="ContentType")
    content_length: int | None = Field(default=None, alias="ContentLength")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    fractielabel: str | None = Field(default=None, alias="Fractielabel")
    activiteit_actor: list[ActiviteitActor] | None = Field(default=None, alias="ActiviteitActor")
    commissie_zetel_vast_persoon: list[CommissieZetelVastPersoon] | None = Field(default=None, alias="CommissieZetelVastPersoon")
    commissie_zetel_vervanger_persoon: list[CommissieZetelVervangerPersoon] | None = Field(default=None, alias="CommissieZetelVervangerPersoon")
    document_actor: list[DocumentActor] | None = Field(default=None, alias="DocumentActor")
    fractie_zetel_persoon: list[FractieZetelPersoon] | None = Field(default=None, alias="FractieZetelPersoon")
    persoon_contactinformatie: list[PersoonContactinformatie] | None = Field(default=None, alias="PersoonContactinformatie")
    persoon_geschenk: list[PersoonGeschenk] | None = Field(default=None, alias="PersoonGeschenk")
    persoon_loopbaan: list[PersoonLoopbaan] | None = Field(default=None, alias="PersoonLoopbaan")
    persoon_nevenfunctie: list[PersoonNevenfunctie] | None = Field(default=None, alias="PersoonNevenfunctie")
    persoon_onderwijs: list[PersoonOnderwijs] | None = Field(default=None, alias="PersoonOnderwijs")
    persoon_reis: list[PersoonReis] | None = Field(default=None, alias="PersoonReis")
    stemming: list[Stemming] | None = Field(default=None, alias="Stemming")
    zaak_actor: list[ZaakActor] | None = Field(default=None, alias="ZaakActor")
    toegezegd_aan: list[ToegezegdAan] | None = Field(default=None, alias="ToegezegdAan")


class PersoonContactinformatie(EntityBase):
    """OData entity type ``PersoonContactinformatie``."""

    id: UUID = Field(alias="Id")
    soort: str | None = Field(default=None, alias="Soort")
    waarde: str | None = Field(default=None, alias="Waarde")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    persoon__id: UUID | None = Field(default=None, alias="Persoon_Id")
    gewicht: int | None = Field(default=None, alias="Gewicht")
    persoon: Persoon | None = Field(default=None, alias="Persoon")


class PersoonGeschenk(EntityBase):
    """OData entity type ``PersoonGeschenk``."""

    id: UUID = Field(alias="Id")
    omschrijving: str | None = Field(default=None, alias="Omschrijving")
    datum: datetime | None = Field(default=None, alias="Datum")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    persoon__id: UUID | None = Field(default=None, alias="Persoon_Id")
    gewicht: int | None = Field(default=None, alias="Gewicht")
    persoon: Persoon | None = Field(default=None, alias="Persoon")


class PersoonLoopbaan(EntityBase):
    """OData entity type ``PersoonLoopbaan``."""

    id: UUID = Field(alias="Id")
    functie: str | None = Field(default=None, alias="Functie")
    werkgever: str | None = Field(default=None, alias="Werkgever")
    omschrijving_nl: str | None = Field(default=None, alias="OmschrijvingNl")
    omschrijving_en: str | None = Field(default=None, alias="OmschrijvingEn")
    plaats: str | None = Field(default=None, alias="Plaats")
    van: str | None = Field(default=None, alias="Van")
    tot_en_met: str | None = Field(default=None, alias="TotEnMet")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    persoon__id: UUID | None = Field(default=None, alias="Persoon_Id")
    gewicht: int | None = Field(default=None, alias="Gewicht")
    persoon: Persoon | None = Field(default=None, alias="Persoon")


class PersoonNevenfunctie(EntityBase):
    """OData entity type ``PersoonNevenfunctie``."""

    id: UUID = Field(alias="Id")
    persoon_id: UUID | None = Field(default=None, alias="PersoonId")
    omschrijving: str | None = Field(default=None, alias="Omschrijving")
    periode_van: str | None = Field(default=None, alias="PeriodeVan")
    periode_tot_en_met: str | None = Field(default=None, alias="PeriodeTotEnMet")
    is_actief: bool | None = Field(default=None, alias="IsActief")
    vergoeding_soort: str | None = Field(default=None, alias="VergoedingSoort")
    vergoeding_toelichting: str | None = Field(default=None, alias="VergoedingToelichting")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    gewicht: int | None = Field(default=None, alias="Gewicht")
    persoon: Persoon | None = Field(default=None, alias="Persoon")
    persoon_nevenfunctie_inkomsten: list[PersoonNevenfunctieInkomsten] | None = Field(default=None, alias="PersoonNevenfunctieInkomsten")


class PersoonNevenfunctieInkomsten(EntityBase):
    """OData entity type ``PersoonNevenfunctieInkomsten``."""

    id: UUID = Field(alias="Id")
    jaar: str | None = Field(default=None, alias="Jaar")
    bedrag_soort: str | None = Field(default=None, alias="BedragSoort")
    bedrag_voorvoegsel: str | None = Field(default=None, alias="BedragVoorvoegsel")
    bedrag_valuta: str | None = Field(default=None, alias="BedragValuta")
    bedrag: float | None = Field(default=None, alias="Bedrag")
    bedrag_achtervoegsel: str | None = Field(default=None, alias="BedragAchtervoegsel")
    frequentie: str | None = Field(default=None, alias="Frequentie")
    frequentie_beschrijving: str | None = Field(default=None, alias="FrequentieBeschrijving")
    opmerking: str | None = Field(default=None, alias="Opmerking")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    nevenfunctie__id: UUID | None = Field(default=None, alias="Nevenfunctie_Id")
    persoon_nevenfunctie: PersoonNevenfunctie | None = Field(default=None, alias="PersoonNevenfunctie")


class PersoonOnderwijs(EntityBase):
    """OData entity type ``PersoonOnderwijs``."""

    id: UUID = Field(alias="Id")
    opleiding_nl: str | None = Field(default=None, alias="OpleidingNl")
    opleiding_en: str | None = Field(default=None, alias="OpleidingEn")
    instelling: str | None = Field(default=None, alias="Instelling")
    plaats: str | None = Field(default=None, alias="Plaats")
    van: str | None = Field(default=None, alias="Van")
    tot_en_met: str | None = Field(default=None, alias="TotEnMet")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    persoon__id: UUID | None = Field(default=None, alias="Persoon_Id")
    gewicht: int | None = Field(default=None, alias="Gewicht")
    persoon: Persoon | None = Field(default=None, alias="Persoon")


class PersoonReis(EntityBase):
    """OData entity type ``PersoonReis``."""

    id: UUID = Field(alias="Id")
    doel: str | None = Field(default=None, alias="Doel")
    bestemming: str | None = Field(default=None, alias="Bestemming")
    van: str | None = Field(default=None, alias="Van")
    tot_en_met: str | None = Field(default=None, alias="TotEnMet")
    betaald_door: str | None = Field(default=None, alias="BetaaldDoor")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    persoon__id: UUID | None = Field(default=None, alias="Persoon_Id")
    gewicht: int | None = Field(default=None, alias="Gewicht")
    persoon: Persoon | None = Field(default=None, alias="Persoon")

