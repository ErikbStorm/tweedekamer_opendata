"""Domain models for fractie entities."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field

from tweedekamer.models.base import EntityBase

if TYPE_CHECKING:
    from tweedekamer.models.activiteit import ActiviteitActor  # noqa: F401
    from tweedekamer.models.commissie import CommissieZetelVastVacature  # noqa: F401
    from tweedekamer.models.commissie import CommissieZetelVervangerVacature  # noqa: F401
    from tweedekamer.models.document import DocumentActor  # noqa: F401
    from tweedekamer.models.persoon import Persoon  # noqa: F401
    from tweedekamer.models.activiteit import Stemming  # noqa: F401
    from tweedekamer.models.zaak import ToegezegdAan  # noqa: F401
    from tweedekamer.models.zaak import ZaakActor  # noqa: F401


class Fractie(EntityBase):
    """OData entity type ``Fractie``."""

    id: UUID = Field(alias="Id")
    nummer: int | None = Field(default=None, alias="Nummer")
    afkorting: str | None = Field(default=None, alias="Afkorting")
    naam_nl: str | None = Field(default=None, alias="NaamNL")
    naam_en: str | None = Field(default=None, alias="NaamEN")
    aantal_zetels: int | None = Field(default=None, alias="AantalZetels")
    aantal_stemmen: int | None = Field(default=None, alias="AantalStemmen")
    datum_actief: datetime | None = Field(default=None, alias="DatumActief")
    datum_inactief: datetime | None = Field(default=None, alias="DatumInactief")
    content_type: str | None = Field(default=None, alias="ContentType")
    content_length: int | None = Field(default=None, alias="ContentLength")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    activiteit_actor: list[ActiviteitActor] | None = Field(default=None, alias="ActiviteitActor")
    commissie_vast_vacature: list[CommissieZetelVastVacature] | None = Field(
        default=None, alias="CommissieVastVacature"
    )
    commissie_vervanger_vacature: list[CommissieZetelVervangerVacature] | None = Field(
        default=None, alias="CommissieVervangerVacature"
    )
    document_actor: list[DocumentActor] | None = Field(default=None, alias="DocumentActor")
    fractie_zetel: list[FractieZetel] | None = Field(default=None, alias="FractieZetel")
    stemming: list[Stemming] | None = Field(default=None, alias="Stemming")
    zaak_actor: list[ZaakActor] | None = Field(default=None, alias="ZaakActor")
    toegezegd_aan: list[ToegezegdAan] | None = Field(default=None, alias="ToegezegdAan")


class FractieZetel(EntityBase):
    """OData entity type ``FractieZetel``."""

    id: UUID = Field(alias="Id")
    gewicht: int | None = Field(default=None, alias="Gewicht")
    fractie__id: UUID | None = Field(default=None, alias="Fractie_Id")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    fractie: Fractie | None = Field(default=None, alias="Fractie")
    fractie_zetel_persoon: list[FractieZetelPersoon] | None = Field(
        default=None, alias="FractieZetelPersoon"
    )
    fractie_zetel_vacature: list[FractieZetelVacature] | None = Field(
        default=None, alias="FractieZetelVacature"
    )


class FractieZetelPersoon(EntityBase):
    """OData entity type ``FractieZetelPersoon``."""

    id: UUID = Field(alias="Id")
    fractie_zetel__id: UUID | None = Field(default=None, alias="FractieZetel_Id")
    persoon__id: UUID | None = Field(default=None, alias="Persoon_Id")
    functie: str | None = Field(default=None, alias="Functie")
    van: datetime | None = Field(default=None, alias="Van")
    tot_en_met: datetime | None = Field(default=None, alias="TotEnMet")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    fractie_zetel: FractieZetel | None = Field(default=None, alias="FractieZetel")
    persoon: Persoon | None = Field(default=None, alias="Persoon")


class FractieZetelVacature(EntityBase):
    """OData entity type ``FractieZetelVacature``."""

    id: UUID = Field(alias="Id")
    fractie_zetel__id: UUID | None = Field(default=None, alias="FractieZetel_Id")
    functie: str | None = Field(default=None, alias="Functie")
    van: datetime | None = Field(default=None, alias="Van")
    tot_en_met: datetime | None = Field(default=None, alias="TotEnMet")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    fractie_zetel: FractieZetel | None = Field(default=None, alias="FractieZetel")
