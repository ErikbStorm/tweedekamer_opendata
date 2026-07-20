"""Domain models for document entities."""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field

from tweedekamer.models.base import EntityBase

if TYPE_CHECKING:
    from tweedekamer.models.activiteit import Activiteit  # noqa: F401
    from tweedekamer.models.activiteit import Agendapunt  # noqa: F401
    from tweedekamer.models.commissie import Commissie  # noqa: F401
    from tweedekamer.models.fractie import Fractie  # noqa: F401
    from tweedekamer.models.persoon import Persoon  # noqa: F401
    from tweedekamer.models.zaak import Zaak  # noqa: F401


class Document(EntityBase):
    """OData entity type ``Document``."""

    id: UUID = Field(alias="Id")
    soort: str | None = Field(default=None, alias="Soort")
    document_nummer: str | None = Field(default=None, alias="DocumentNummer")
    titel: str | None = Field(default=None, alias="Titel")
    onderwerp: str | None = Field(default=None, alias="Onderwerp")
    datum: datetime | None = Field(default=None, alias="Datum")
    vergaderjaar: str | None = Field(default=None, alias="Vergaderjaar")
    kamer: int | None = Field(default=None, alias="Kamer")
    volgnummer: int | None = Field(default=None, alias="Volgnummer")
    citeertitel: str | None = Field(default=None, alias="Citeertitel")
    alias: str | None = Field(default=None, alias="Alias")
    datum_registratie: datetime | None = Field(default=None, alias="DatumRegistratie")
    datum_ontvangst: datetime | None = Field(default=None, alias="DatumOntvangst")
    aanhangselnummer: str | None = Field(default=None, alias="Aanhangselnummer")
    kenmerk_afzender: str | None = Field(default=None, alias="KenmerkAfzender")
    organisatie: str | None = Field(default=None, alias="Organisatie")
    content_type: str | None = Field(default=None, alias="ContentType")
    content_length: int | None = Field(default=None, alias="ContentLength")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    huidige_document_versie__id: UUID | None = Field(default=None, alias="HuidigeDocumentVersie_Id")
    document_actor: list[DocumentActor] | None = Field(default=None, alias="DocumentActor")
    document_versie: list[DocumentVersie] | None = Field(default=None, alias="DocumentVersie")
    huidige_document_versie: DocumentVersie | None = Field(default=None, alias="HuidigeDocumentVersie")
    activiteit: list[Activiteit] | None = Field(default=None, alias="Activiteit")
    agendapunt: list[Agendapunt] | None = Field(default=None, alias="Agendapunt")
    bijlage_document: list[Document] | None = Field(default=None, alias="BijlageDocument")
    bron_document: list[Document] | None = Field(default=None, alias="BronDocument")
    kamerstukdossier: list[Kamerstukdossier] | None = Field(default=None, alias="Kamerstukdossier")
    zaak: list[Zaak] | None = Field(default=None, alias="Zaak")


class DocumentActor(EntityBase):
    """OData entity type ``DocumentActor``."""

    id: UUID = Field(alias="Id")
    document__id: UUID | None = Field(default=None, alias="Document_Id")
    actor_naam: str | None = Field(default=None, alias="ActorNaam")
    actor_fractie: str | None = Field(default=None, alias="ActorFractie")
    functie: str | None = Field(default=None, alias="Functie")
    relatie: str | None = Field(default=None, alias="Relatie")
    sid_actor: str | None = Field(default=None, alias="SidActor")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    persoon__id: UUID | None = Field(default=None, alias="Persoon_Id")
    fractie__id: UUID | None = Field(default=None, alias="Fractie_Id")
    commissie__id: UUID | None = Field(default=None, alias="Commissie_Id")
    commissie: Commissie | None = Field(default=None, alias="Commissie")
    document: Document | None = Field(default=None, alias="Document")
    fractie: Fractie | None = Field(default=None, alias="Fractie")
    persoon: Persoon | None = Field(default=None, alias="Persoon")


class DocumentVersie(EntityBase):
    """OData entity type ``DocumentVersie``."""

    id: UUID = Field(alias="Id")
    status: str | None = Field(default=None, alias="Status")
    versienummer: int | None = Field(default=None, alias="Versienummer")
    bestandsgrootte: int | None = Field(default=None, alias="Bestandsgrootte")
    extensie: str | None = Field(default=None, alias="Extensie")
    datum: datetime | None = Field(default=None, alias="Datum")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    document__id: UUID | None = Field(default=None, alias="Document_Id")
    externe_identifier: str | None = Field(default=None, alias="ExterneIdentifier")
    document: Document | None = Field(default=None, alias="Document")
    document_publicatie: list[DocumentPublicatie] | None = Field(default=None, alias="DocumentPublicatie")
    document_publicatie_metadata: list[DocumentPublicatieMetadata] | None = Field(default=None, alias="DocumentPublicatieMetadata")


class DocumentPublicatie(EntityBase):
    """OData entity type ``DocumentPublicatie``."""

    id: UUID = Field(alias="Id")
    identifier: str | None = Field(default=None, alias="Identifier")
    document_type: str | None = Field(default=None, alias="DocumentType")
    file_name: str | None = Field(default=None, alias="FileName")
    source: str | None = Field(default=None, alias="Source")
    content_length: int | None = Field(default=None, alias="ContentLength")
    content_type: str | None = Field(default=None, alias="ContentType")
    url: str | None = Field(default=None, alias="Url")
    publicatie_datum: datetime | None = Field(default=None, alias="PublicatieDatum")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    document_versie__id: UUID | None = Field(default=None, alias="DocumentVersie_Id")
    document_versie: DocumentVersie | None = Field(default=None, alias="DocumentVersie")


class DocumentPublicatieMetadata(EntityBase):
    """OData entity type ``DocumentPublicatieMetadata``."""

    id: UUID = Field(alias="Id")
    identifier: str | None = Field(default=None, alias="Identifier")
    document_type: str | None = Field(default=None, alias="DocumentType")
    file_name: str | None = Field(default=None, alias="FileName")
    source: str | None = Field(default=None, alias="Source")
    content_length: int | None = Field(default=None, alias="ContentLength")
    content_type: str | None = Field(default=None, alias="ContentType")
    url: str | None = Field(default=None, alias="Url")
    publicatie_datum: datetime | None = Field(default=None, alias="PublicatieDatum")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    document_versie__id: UUID | None = Field(default=None, alias="DocumentVersie_Id")
    document_versie: DocumentVersie | None = Field(default=None, alias="DocumentVersie")


class Kamerstukdossier(EntityBase):
    """OData entity type ``Kamerstukdossier``."""

    id: UUID = Field(alias="Id")
    titel: str | None = Field(default=None, alias="Titel")
    citeertitel: str | None = Field(default=None, alias="Citeertitel")
    alias: str | None = Field(default=None, alias="Alias")
    nummer: int | None = Field(default=None, alias="Nummer")
    toevoeging: str | None = Field(default=None, alias="Toevoeging")
    hoogste_volgnummer: int | None = Field(default=None, alias="HoogsteVolgnummer")
    afgesloten: bool | None = Field(default=None, alias="Afgesloten")
    kamer: str | None = Field(default=None, alias="Kamer")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    document: list[Document] | None = Field(default=None, alias="Document")
    zaak: list[Zaak] | None = Field(default=None, alias="Zaak")

