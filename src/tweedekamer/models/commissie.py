"""Domain models for commissie entities."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field

from tweedekamer.models.base import EntityBase

if TYPE_CHECKING:
    from tweedekamer.models.activiteit import Activiteit  # noqa: F401
    from tweedekamer.models.activiteit import ActiviteitActor  # noqa: F401
    from tweedekamer.models.document import DocumentActor  # noqa: F401
    from tweedekamer.models.fractie import Fractie  # noqa: F401
    from tweedekamer.models.persoon import Persoon  # noqa: F401
    from tweedekamer.models.zaak import ZaakActor  # noqa: F401


class Commissie(EntityBase):
    """OData entity type ``Commissie``."""

    id: UUID = Field(alias="Id")
    nummer: int | None = Field(default=None, alias="Nummer")
    soort: str | None = Field(default=None, alias="Soort")
    afkorting: str | None = Field(default=None, alias="Afkorting")
    naam_nl: str | None = Field(default=None, alias="NaamNL")
    naam_en: str | None = Field(default=None, alias="NaamEN")
    naam_web_nl: str | None = Field(default=None, alias="NaamWebNL")
    naam_web_en: str | None = Field(default=None, alias="NaamWebEN")
    inhoudsopgave: str | None = Field(default=None, alias="Inhoudsopgave")
    datum_actief: datetime | None = Field(default=None, alias="DatumActief")
    datum_inactief: datetime | None = Field(default=None, alias="DatumInactief")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    activiteit: list[Activiteit] | None = Field(default=None, alias="Activiteit")
    activiteit_actor: list[ActiviteitActor] | None = Field(default=None, alias="ActiviteitActor")
    commissie_contactinformatie: list[CommissieContactinformatie] | None = Field(
        default=None, alias="CommissieContactinformatie"
    )
    commissie_zetel: list[CommissieZetel] | None = Field(default=None, alias="CommissieZetel")
    document_actor: list[DocumentActor] | None = Field(default=None, alias="DocumentActor")
    zaak_actor: list[ZaakActor] | None = Field(default=None, alias="ZaakActor")


class CommissieContactinformatie(EntityBase):
    """OData entity type ``CommissieContactinformatie``."""

    id: UUID = Field(alias="Id")
    soort: str | None = Field(default=None, alias="Soort")
    waarde: str | None = Field(default=None, alias="Waarde")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    commissie__id: UUID | None = Field(default=None, alias="Commissie_Id")
    commissie: Commissie | None = Field(default=None, alias="Commissie")


class CommissieZetel(EntityBase):
    """OData entity type ``CommissieZetel``."""

    id: UUID = Field(alias="Id")
    gewicht: int | None = Field(default=None, alias="Gewicht")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    commissie__id: UUID | None = Field(default=None, alias="Commissie_Id")
    commissie: Commissie | None = Field(default=None, alias="Commissie")
    commissie_zetel_vast_persoon: list[CommissieZetelVastPersoon] | None = Field(
        default=None, alias="CommissieZetelVastPersoon"
    )
    commissie_zetel_vast_vacature: list[CommissieZetelVastVacature] | None = Field(
        default=None, alias="CommissieZetelVastVacature"
    )
    commissie_zetel_vervanger_persoon: list[CommissieZetelVervangerPersoon] | None = Field(
        default=None, alias="CommissieZetelVervangerPersoon"
    )
    commissie_zetel_vervanger_vacature: list[CommissieZetelVervangerVacature] | None = Field(
        default=None, alias="CommissieZetelVervangerVacature"
    )


class CommissieZetelVastPersoon(EntityBase):
    """OData entity type ``CommissieZetelVastPersoon``."""

    id: UUID = Field(alias="Id")
    functie: str | None = Field(default=None, alias="Functie")
    van: datetime | None = Field(default=None, alias="Van")
    tot_en_met: datetime | None = Field(default=None, alias="TotEnMet")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    commissie_zetel__id: UUID | None = Field(default=None, alias="CommissieZetel_Id")
    persoon__id: UUID | None = Field(default=None, alias="Persoon_Id")
    commissie_zetel: CommissieZetel | None = Field(default=None, alias="CommissieZetel")
    persoon: Persoon | None = Field(default=None, alias="Persoon")


class CommissieZetelVastVacature(EntityBase):
    """OData entity type ``CommissieZetelVastVacature``."""

    id: UUID = Field(alias="Id")
    functie: str | None = Field(default=None, alias="Functie")
    van: datetime | None = Field(default=None, alias="Van")
    tot_en_met: datetime | None = Field(default=None, alias="TotEnMet")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    commissie_zetel__id: UUID | None = Field(default=None, alias="CommissieZetel_Id")
    fractie__id: UUID | None = Field(default=None, alias="Fractie_Id")
    commissie_zetel: CommissieZetel | None = Field(default=None, alias="CommissieZetel")
    fractie: Fractie | None = Field(default=None, alias="Fractie")


class CommissieZetelVervangerPersoon(EntityBase):
    """OData entity type ``CommissieZetelVervangerPersoon``."""

    id: UUID = Field(alias="Id")
    functie: str | None = Field(default=None, alias="Functie")
    van: datetime | None = Field(default=None, alias="Van")
    tot_en_met: datetime | None = Field(default=None, alias="TotEnMet")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    commissie_zetel__id: UUID | None = Field(default=None, alias="CommissieZetel_Id")
    persoon__id: UUID | None = Field(default=None, alias="Persoon_Id")
    commissie_zetel: CommissieZetel | None = Field(default=None, alias="CommissieZetel")
    persoon: Persoon | None = Field(default=None, alias="Persoon")


class CommissieZetelVervangerVacature(EntityBase):
    """OData entity type ``CommissieZetelVervangerVacature``."""

    id: UUID = Field(alias="Id")
    functie: str | None = Field(default=None, alias="Functie")
    van: datetime | None = Field(default=None, alias="Van")
    tot_en_met: datetime | None = Field(default=None, alias="TotEnMet")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    commissie_zetel__id: UUID | None = Field(default=None, alias="CommissieZetel_Id")
    fractie__id: UUID | None = Field(default=None, alias="Fractie_Id")
    commissie_zetel: CommissieZetel | None = Field(default=None, alias="CommissieZetel")
    fractie: Fractie | None = Field(default=None, alias="Fractie")
