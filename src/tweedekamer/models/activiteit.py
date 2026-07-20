"""Domain models for activiteit entities."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from pydantic import Field

from tweedekamer.models.base import EntityBase

if TYPE_CHECKING:
    from tweedekamer.models.commissie import Commissie  # noqa: F401
    from tweedekamer.models.document import Document  # noqa: F401
    from tweedekamer.models.fractie import Fractie  # noqa: F401
    from tweedekamer.models.persoon import Persoon  # noqa: F401
    from tweedekamer.models.zaak import Toezegging  # noqa: F401
    from tweedekamer.models.zaak import Zaak  # noqa: F401


class Activiteit(EntityBase):
    """OData entity type ``Activiteit``."""

    id: UUID = Field(alias="Id")
    soort: str | None = Field(default=None, alias="Soort")
    nummer: str | None = Field(default=None, alias="Nummer")
    onderwerp: str | None = Field(default=None, alias="Onderwerp")
    datum_soort: str | None = Field(default=None, alias="DatumSoort")
    datum: datetime | None = Field(default=None, alias="Datum")
    aanvangstijd: datetime | None = Field(default=None, alias="Aanvangstijd")
    eindtijd: datetime | None = Field(default=None, alias="Eindtijd")
    locatie: str | None = Field(default=None, alias="Locatie")
    besloten: bool | None = Field(default=None, alias="Besloten")
    status: str | None = Field(default=None, alias="Status")
    vergaderjaar: str | None = Field(default=None, alias="Vergaderjaar")
    kamer: str | None = Field(default=None, alias="Kamer")
    noot: str | None = Field(default=None, alias="Noot")
    vrs_nummer: str | None = Field(default=None, alias="VRSNummer")
    sid_voortouw: str | None = Field(default=None, alias="SidVoortouw")
    voortouwnaam: str | None = Field(default=None, alias="Voortouwnaam")
    voortouwafkorting: str | None = Field(default=None, alias="Voortouwafkorting")
    voortouwkortenaam: str | None = Field(default=None, alias="Voortouwkortenaam")
    voortouwcommissie__id: UUID | None = Field(default=None, alias="Voortouwcommissie_Id")
    aanvraagdatum: datetime | None = Field(default=None, alias="Aanvraagdatum")
    datum_verzoek_eerste_verlenging: datetime | None = Field(
        default=None, alias="DatumVerzoekEersteVerlenging"
    )
    datum_mededeling_eerste_verlenging: datetime | None = Field(
        default=None, alias="DatumMededelingEersteVerlenging"
    )
    datum_verzoek_tweede_verlenging: datetime | None = Field(
        default=None, alias="DatumVerzoekTweedeVerlenging"
    )
    datum_mededeling_tweede_verlenging: datetime | None = Field(
        default=None, alias="DatumMededelingTweedeVerlenging"
    )
    vervaldatum: datetime | None = Field(default=None, alias="Vervaldatum")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    voortouwcommissie: Commissie | None = Field(default=None, alias="Voortouwcommissie")
    activiteit_actor: list[ActiviteitActor] | None = Field(default=None, alias="ActiviteitActor")
    agendapunt: list[Agendapunt] | None = Field(default=None, alias="Agendapunt")
    voortgezet_in: list[Activiteit] | None = Field(default=None, alias="VoortgezetIn")
    vervangen_door: list[Activiteit] | None = Field(default=None, alias="VervangenDoor")
    vervangen_vanuit: list[Activiteit] | None = Field(default=None, alias="VervangenVanuit")
    voortgezet_vanuit: list[Activiteit] | None = Field(default=None, alias="VoortgezetVanuit")
    document: list[Document] | None = Field(default=None, alias="Document")
    reservering: list[Reservering] | None = Field(default=None, alias="Reservering")
    toezegging: list[Toezegging] | None = Field(default=None, alias="Toezegging")
    zaak: list[Zaak] | None = Field(default=None, alias="Zaak")


class ActiviteitActor(EntityBase):
    """OData entity type ``ActiviteitActor``."""

    id: UUID = Field(alias="Id")
    activiteit__id: UUID | None = Field(default=None, alias="Activiteit_Id")
    actor_naam: str | None = Field(default=None, alias="ActorNaam")
    actor_fractie: str | None = Field(default=None, alias="ActorFractie")
    relatie: str | None = Field(default=None, alias="Relatie")
    volgorde: int | None = Field(default=None, alias="Volgorde")
    functie: str | None = Field(default=None, alias="Functie")
    spreektijd: str | None = Field(default=None, alias="Spreektijd")
    sid_actor: str | None = Field(default=None, alias="SidActor")
    persoon__id: UUID | None = Field(default=None, alias="Persoon_Id")
    fractie__id: UUID | None = Field(default=None, alias="Fractie_Id")
    commissie__id: UUID | None = Field(default=None, alias="Commissie_Id")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    activiteit: Activiteit | None = Field(default=None, alias="Activiteit")
    commissie: Commissie | None = Field(default=None, alias="Commissie")
    fractie: Fractie | None = Field(default=None, alias="Fractie")
    persoon: Persoon | None = Field(default=None, alias="Persoon")


class Agendapunt(EntityBase):
    """OData entity type ``Agendapunt``."""

    id: UUID = Field(alias="Id")
    nummer: str | None = Field(default=None, alias="Nummer")
    onderwerp: str | None = Field(default=None, alias="Onderwerp")
    aanvangstijd: datetime | None = Field(default=None, alias="Aanvangstijd")
    eindtijd: datetime | None = Field(default=None, alias="Eindtijd")
    volgorde: int | None = Field(default=None, alias="Volgorde")
    rubriek: str | None = Field(default=None, alias="Rubriek")
    noot: str | None = Field(default=None, alias="Noot")
    status: str | None = Field(default=None, alias="Status")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    activiteit__id: UUID | None = Field(default=None, alias="Activiteit_Id")
    activiteit: Activiteit | None = Field(default=None, alias="Activiteit")
    besluit: list[Besluit] | None = Field(default=None, alias="Besluit")
    document: list[Document] | None = Field(default=None, alias="Document")
    zaak: list[Zaak] | None = Field(default=None, alias="Zaak")


class Besluit(EntityBase):
    """OData entity type ``Besluit``."""

    id: UUID = Field(alias="Id")
    agendapunt__id: UUID | None = Field(default=None, alias="Agendapunt_Id")
    stemmings_soort: str | None = Field(default=None, alias="StemmingsSoort")
    besluit_soort: str | None = Field(default=None, alias="BesluitSoort")
    besluit_tekst: str | None = Field(default=None, alias="BesluitTekst")
    opmerking: str | None = Field(default=None, alias="Opmerking")
    status: str | None = Field(default=None, alias="Status")
    agendapunt_zaak_besluit_volgorde: int | None = Field(
        default=None, alias="AgendapuntZaakBesluitVolgorde"
    )
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    agendapunt: Agendapunt | None = Field(default=None, alias="Agendapunt")
    stemming: list[Stemming] | None = Field(default=None, alias="Stemming")
    zaak: list[Zaak] | None = Field(default=None, alias="Zaak")


class Stemming(EntityBase):
    """OData entity type ``Stemming``."""

    id: UUID = Field(alias="Id")
    besluit__id: UUID | None = Field(default=None, alias="Besluit_Id")
    soort: str | None = Field(default=None, alias="Soort")
    fractie_grootte: int | None = Field(default=None, alias="FractieGrootte")
    actor_naam: str | None = Field(default=None, alias="ActorNaam")
    actor_fractie: str | None = Field(default=None, alias="ActorFractie")
    vergissing: bool | None = Field(default=None, alias="Vergissing")
    sid_actor_lid: str | None = Field(default=None, alias="SidActorLid")
    sid_actor_fractie: str | None = Field(default=None, alias="SidActorFractie")
    persoon__id: UUID | None = Field(default=None, alias="Persoon_Id")
    fractie__id: UUID | None = Field(default=None, alias="Fractie_Id")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    besluit: Besluit | None = Field(default=None, alias="Besluit")
    fractie: Fractie | None = Field(default=None, alias="Fractie")
    persoon: Persoon | None = Field(default=None, alias="Persoon")


class Vergadering(EntityBase):
    """OData entity type ``Vergadering``."""

    id: UUID = Field(alias="Id")
    soort: str | None = Field(default=None, alias="Soort")
    titel: str | None = Field(default=None, alias="Titel")
    zaal: str | None = Field(default=None, alias="Zaal")
    vergaderjaar: str | None = Field(default=None, alias="Vergaderjaar")
    vergadering_nummer: int | None = Field(default=None, alias="VergaderingNummer")
    datum: datetime | None = Field(default=None, alias="Datum")
    aanvangstijd: datetime | None = Field(default=None, alias="Aanvangstijd")
    sluiting: datetime | None = Field(default=None, alias="Sluiting")
    kamer: str | None = Field(default=None, alias="Kamer")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    verslag: list[Verslag] | None = Field(default=None, alias="Verslag")


class Verslag(EntityBase):
    """OData entity type ``Verslag``."""

    id: UUID = Field(alias="Id")
    soort: str | None = Field(default=None, alias="Soort")
    status: str | None = Field(default=None, alias="Status")
    content_type: str | None = Field(default=None, alias="ContentType")
    content_length: int | None = Field(default=None, alias="ContentLength")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    vergadering__id: UUID | None = Field(default=None, alias="Vergadering_Id")
    vergadering: Vergadering | None = Field(default=None, alias="Vergadering")


class Zaal(EntityBase):
    """OData entity type ``Zaal``."""

    id: UUID = Field(alias="Id")
    naam: str | None = Field(default=None, alias="Naam")
    sys_code: int | None = Field(default=None, alias="SysCode")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    reservering: list[Reservering] | None = Field(default=None, alias="Reservering")


class Reservering(EntityBase):
    """OData entity type ``Reservering``."""

    id: UUID = Field(alias="Id")
    nummer: str | None = Field(default=None, alias="Nummer")
    status_code: str | None = Field(default=None, alias="StatusCode")
    status_naam: str | None = Field(default=None, alias="StatusNaam")
    gewijzigd_op: datetime | None = Field(default=None, alias="GewijzigdOp")
    api_gewijzigd_op: datetime | None = Field(default=None, alias="ApiGewijzigdOp")
    verwijderd: bool | None = Field(default=None, alias="Verwijderd")
    activiteit_nummer: str | None = Field(default=None, alias="ActiviteitNummer")
    activiteit: list[Activiteit] | None = Field(default=None, alias="Activiteit")
    zaal: list[Zaal] | None = Field(default=None, alias="Zaal")
