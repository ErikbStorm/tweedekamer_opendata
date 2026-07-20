"""OData client for the Tweede Kamer Gegevensmagazijn."""

from __future__ import annotations

from types import TracebackType
from typing import Any, TypeVar

import httpx

from tweedekamer._http import (
    DEFAULT_ODATA_BASE,
    DEFAULT_TIMEOUT,
    default_user_agent,
    ensure_client,
)
from tweedekamer._version import __version__
from tweedekamer.models import ENTITY_MODELS, EntityBase
from tweedekamer.models.activiteit import (
    Activiteit,
    ActiviteitActor,
    Agendapunt,
    Besluit,
    Reservering,
    Stemming,
    Vergadering,
    Verslag,
    Zaal,
)
from tweedekamer.models.commissie import (
    Commissie,
    CommissieContactinformatie,
    CommissieZetel,
    CommissieZetelVastPersoon,
    CommissieZetelVastVacature,
    CommissieZetelVervangerPersoon,
    CommissieZetelVervangerVacature,
)
from tweedekamer.models.document import (
    Document,
    DocumentActor,
    DocumentPublicatie,
    DocumentPublicatieMetadata,
    DocumentVersie,
    Kamerstukdossier,
)
from tweedekamer.models.fractie import (
    Fractie,
    FractieZetel,
    FractieZetelPersoon,
    FractieZetelVacature,
)
from tweedekamer.models.persoon import (
    Persoon,
    PersoonContactinformatie,
    PersoonGeschenk,
    PersoonLoopbaan,
    PersoonNevenfunctie,
    PersoonNevenfunctieInkomsten,
    PersoonOnderwijs,
    PersoonReis,
)
from tweedekamer.models.zaak import ToegezegdAan, Toezegging, Zaak, ZaakActor
from tweedekamer.query import ODataQuery

T = TypeVar("T", bound=EntityBase)


class Client:
    """High-level OData client for parliamentary open data.

    Example:
        >>> from tweedekamer import Client
        >>> client = Client()
        >>> people = client.personen.exclude_deleted().top(5).all()
    """

    def __init__(
        self,
        *,
        base_url: str = DEFAULT_ODATA_BASE,
        timeout: float = DEFAULT_TIMEOUT,
        user_agent: str | None = None,
        metadata_level: str = "none",
        http_client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.metadata_level = metadata_level
        self._headers = {
            "User-Agent": user_agent or default_user_agent(__version__),
            "Accept": "application/json",
        }
        self._http, self._owns_client = ensure_client(
            http_client,
            timeout=timeout,
            headers=self._headers,
        )

    def close(self) -> None:
        """Close the underlying HTTP client if owned by this instance."""
        if self._owns_client:
            self._http.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.close()

    def entity(self, name: str, model: type[T] | None = None) -> ODataQuery[T]:
        """Return a query builder for an arbitrary entity set.

        Args:
            name: Entity set name as used by the API (e.g. ``\"Zaak\"``).
            model: Optional Pydantic model. Defaults to the known model for
                ``name``, or :class:`~tweedekamer.models.base.EntityBase`.
        """
        resolved: type[EntityBase]
        if model is not None:
            resolved = model
        elif name in ENTITY_MODELS:
            resolved = ENTITY_MODELS[name]
        else:
            resolved = EntityBase
        return ODataQuery(
            http=self._http,
            base_url=self.base_url,
            entity_set=name,
            model=resolved,  # type: ignore[arg-type]
            metadata_level=self.metadata_level,
        )

    def entity_sets(self) -> list[str]:
        """List entity set names from the service document."""
        response = self._http.get(
            self.base_url,
            params={"$format": "application/json;odata.metadata=minimal"},
        )
        response.raise_for_status()
        data: dict[str, Any] = response.json()
        return [item["name"] for item in data.get("value", []) if item.get("kind") == "EntitySet"]

    # -- typed entity-set accessors ----------------------------------------

    @property
    def personen(self) -> ODataQuery[Persoon]:
        return self.entity("Persoon", Persoon)

    @property
    def persoon_contactinformatie(self) -> ODataQuery[PersoonContactinformatie]:
        return self.entity("PersoonContactinformatie", PersoonContactinformatie)

    @property
    def persoon_geschenken(self) -> ODataQuery[PersoonGeschenk]:
        return self.entity("PersoonGeschenk", PersoonGeschenk)

    @property
    def persoon_loopbanen(self) -> ODataQuery[PersoonLoopbaan]:
        return self.entity("PersoonLoopbaan", PersoonLoopbaan)

    @property
    def persoon_nevenfuncties(self) -> ODataQuery[PersoonNevenfunctie]:
        return self.entity("PersoonNevenfunctie", PersoonNevenfunctie)

    @property
    def persoon_nevenfunctie_inkomsten(self) -> ODataQuery[PersoonNevenfunctieInkomsten]:
        return self.entity("PersoonNevenfunctieInkomsten", PersoonNevenfunctieInkomsten)

    @property
    def persoon_onderwijs(self) -> ODataQuery[PersoonOnderwijs]:
        return self.entity("PersoonOnderwijs", PersoonOnderwijs)

    @property
    def persoon_reizen(self) -> ODataQuery[PersoonReis]:
        return self.entity("PersoonReis", PersoonReis)

    @property
    def commissies(self) -> ODataQuery[Commissie]:
        return self.entity("Commissie", Commissie)

    @property
    def commissie_contactinformatie(self) -> ODataQuery[CommissieContactinformatie]:
        return self.entity("CommissieContactinformatie", CommissieContactinformatie)

    @property
    def commissie_zetels(self) -> ODataQuery[CommissieZetel]:
        return self.entity("CommissieZetel", CommissieZetel)

    @property
    def commissie_zetel_vast_personen(self) -> ODataQuery[CommissieZetelVastPersoon]:
        return self.entity("CommissieZetelVastPersoon", CommissieZetelVastPersoon)

    @property
    def commissie_zetel_vast_vacatures(self) -> ODataQuery[CommissieZetelVastVacature]:
        return self.entity("CommissieZetelVastVacature", CommissieZetelVastVacature)

    @property
    def commissie_zetel_vervanger_personen(self) -> ODataQuery[CommissieZetelVervangerPersoon]:
        return self.entity("CommissieZetelVervangerPersoon", CommissieZetelVervangerPersoon)

    @property
    def commissie_zetel_vervanger_vacatures(self) -> ODataQuery[CommissieZetelVervangerVacature]:
        return self.entity("CommissieZetelVervangerVacature", CommissieZetelVervangerVacature)

    @property
    def fracties(self) -> ODataQuery[Fractie]:
        return self.entity("Fractie", Fractie)

    @property
    def fractie_zetels(self) -> ODataQuery[FractieZetel]:
        return self.entity("FractieZetel", FractieZetel)

    @property
    def fractie_zetel_personen(self) -> ODataQuery[FractieZetelPersoon]:
        return self.entity("FractieZetelPersoon", FractieZetelPersoon)

    @property
    def fractie_zetel_vacatures(self) -> ODataQuery[FractieZetelVacature]:
        return self.entity("FractieZetelVacature", FractieZetelVacature)

    @property
    def activiteiten(self) -> ODataQuery[Activiteit]:
        return self.entity("Activiteit", Activiteit)

    @property
    def activiteit_actors(self) -> ODataQuery[ActiviteitActor]:
        return self.entity("ActiviteitActor", ActiviteitActor)

    @property
    def agendapunten(self) -> ODataQuery[Agendapunt]:
        return self.entity("Agendapunt", Agendapunt)

    @property
    def besluiten(self) -> ODataQuery[Besluit]:
        return self.entity("Besluit", Besluit)

    @property
    def stemmingen(self) -> ODataQuery[Stemming]:
        return self.entity("Stemming", Stemming)

    @property
    def zaken(self) -> ODataQuery[Zaak]:
        return self.entity("Zaak", Zaak)

    @property
    def zaak_actors(self) -> ODataQuery[ZaakActor]:
        return self.entity("ZaakActor", ZaakActor)

    @property
    def zalen(self) -> ODataQuery[Zaal]:
        return self.entity("Zaal", Zaal)

    @property
    def reserveringen(self) -> ODataQuery[Reservering]:
        return self.entity("Reservering", Reservering)

    @property
    def documenten(self) -> ODataQuery[Document]:
        return self.entity("Document", Document)

    @property
    def document_actors(self) -> ODataQuery[DocumentActor]:
        return self.entity("DocumentActor", DocumentActor)

    @property
    def document_versies(self) -> ODataQuery[DocumentVersie]:
        return self.entity("DocumentVersie", DocumentVersie)

    @property
    def document_publicaties(self) -> ODataQuery[DocumentPublicatie]:
        return self.entity("DocumentPublicatie", DocumentPublicatie)

    @property
    def document_publicatie_metadata(self) -> ODataQuery[DocumentPublicatieMetadata]:
        return self.entity("DocumentPublicatieMetadata", DocumentPublicatieMetadata)

    @property
    def kamerstukdossiers(self) -> ODataQuery[Kamerstukdossier]:
        return self.entity("Kamerstukdossier", Kamerstukdossier)

    @property
    def vergaderingen(self) -> ODataQuery[Vergadering]:
        return self.entity("Vergadering", Vergadering)

    @property
    def verslagen(self) -> ODataQuery[Verslag]:
        return self.entity("Verslag", Verslag)

    @property
    def toezeggingen(self) -> ODataQuery[Toezegging]:
        return self.entity("Toezegging", Toezegging)

    @property
    def toegezegd_aan(self) -> ODataQuery[ToegezegdAan]:
        return self.entity("ToegezegdAan", ToegezegdAan)
