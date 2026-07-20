"""Pydantic models for Tweede Kamer OData entities."""

from __future__ import annotations

from tweedekamer.models.base import EntityBase
from tweedekamer.models.persoon import Persoon
from tweedekamer.models.persoon import PersoonContactinformatie
from tweedekamer.models.persoon import PersoonGeschenk
from tweedekamer.models.persoon import PersoonLoopbaan
from tweedekamer.models.persoon import PersoonNevenfunctie
from tweedekamer.models.persoon import PersoonNevenfunctieInkomsten
from tweedekamer.models.persoon import PersoonOnderwijs
from tweedekamer.models.persoon import PersoonReis
from tweedekamer.models.commissie import Commissie
from tweedekamer.models.commissie import CommissieContactinformatie
from tweedekamer.models.commissie import CommissieZetel
from tweedekamer.models.commissie import CommissieZetelVastPersoon
from tweedekamer.models.commissie import CommissieZetelVastVacature
from tweedekamer.models.commissie import CommissieZetelVervangerPersoon
from tweedekamer.models.commissie import CommissieZetelVervangerVacature
from tweedekamer.models.fractie import Fractie
from tweedekamer.models.fractie import FractieZetel
from tweedekamer.models.fractie import FractieZetelPersoon
from tweedekamer.models.fractie import FractieZetelVacature
from tweedekamer.models.activiteit import Activiteit
from tweedekamer.models.activiteit import ActiviteitActor
from tweedekamer.models.activiteit import Agendapunt
from tweedekamer.models.activiteit import Besluit
from tweedekamer.models.activiteit import Stemming
from tweedekamer.models.activiteit import Vergadering
from tweedekamer.models.activiteit import Verslag
from tweedekamer.models.activiteit import Zaal
from tweedekamer.models.activiteit import Reservering
from tweedekamer.models.zaak import Zaak
from tweedekamer.models.zaak import ZaakActor
from tweedekamer.models.zaak import Toezegging
from tweedekamer.models.zaak import ToegezegdAan
from tweedekamer.models.document import Document
from tweedekamer.models.document import DocumentActor
from tweedekamer.models.document import DocumentVersie
from tweedekamer.models.document import DocumentPublicatie
from tweedekamer.models.document import DocumentPublicatieMetadata
from tweedekamer.models.document import Kamerstukdossier

ENTITY_MODELS: dict[str, type[EntityBase]] = {
    "Persoon": Persoon,
    "PersoonContactinformatie": PersoonContactinformatie,
    "PersoonGeschenk": PersoonGeschenk,
    "PersoonLoopbaan": PersoonLoopbaan,
    "PersoonNevenfunctie": PersoonNevenfunctie,
    "PersoonNevenfunctieInkomsten": PersoonNevenfunctieInkomsten,
    "PersoonOnderwijs": PersoonOnderwijs,
    "PersoonReis": PersoonReis,
    "Commissie": Commissie,
    "CommissieContactinformatie": CommissieContactinformatie,
    "CommissieZetel": CommissieZetel,
    "CommissieZetelVastPersoon": CommissieZetelVastPersoon,
    "CommissieZetelVastVacature": CommissieZetelVastVacature,
    "CommissieZetelVervangerPersoon": CommissieZetelVervangerPersoon,
    "CommissieZetelVervangerVacature": CommissieZetelVervangerVacature,
    "Fractie": Fractie,
    "FractieZetel": FractieZetel,
    "FractieZetelPersoon": FractieZetelPersoon,
    "FractieZetelVacature": FractieZetelVacature,
    "Activiteit": Activiteit,
    "ActiviteitActor": ActiviteitActor,
    "Agendapunt": Agendapunt,
    "Besluit": Besluit,
    "Stemming": Stemming,
    "Vergadering": Vergadering,
    "Verslag": Verslag,
    "Zaal": Zaal,
    "Reservering": Reservering,
    "Zaak": Zaak,
    "ZaakActor": ZaakActor,
    "Toezegging": Toezegging,
    "ToegezegdAan": ToegezegdAan,
    "Document": Document,
    "DocumentActor": DocumentActor,
    "DocumentVersie": DocumentVersie,
    "DocumentPublicatie": DocumentPublicatie,
    "DocumentPublicatieMetadata": DocumentPublicatieMetadata,
    "Kamerstukdossier": Kamerstukdossier,
}

# Resolve cross-module forward references for $expand navigation properties
_ns = {name: cls for name, cls in ENTITY_MODELS.items()}
for _cls in ENTITY_MODELS.values():
    _cls.model_rebuild(_types_namespace=_ns)

__all__ = [
    "EntityBase",
    "ENTITY_MODELS",
    "Persoon",
    "PersoonContactinformatie",
    "PersoonGeschenk",
    "PersoonLoopbaan",
    "PersoonNevenfunctie",
    "PersoonNevenfunctieInkomsten",
    "PersoonOnderwijs",
    "PersoonReis",
    "Commissie",
    "CommissieContactinformatie",
    "CommissieZetel",
    "CommissieZetelVastPersoon",
    "CommissieZetelVastVacature",
    "CommissieZetelVervangerPersoon",
    "CommissieZetelVervangerVacature",
    "Fractie",
    "FractieZetel",
    "FractieZetelPersoon",
    "FractieZetelVacature",
    "Activiteit",
    "ActiviteitActor",
    "Agendapunt",
    "Besluit",
    "Stemming",
    "Vergadering",
    "Verslag",
    "Zaal",
    "Reservering",
    "Zaak",
    "ZaakActor",
    "Toezegging",
    "ToegezegdAan",
    "Document",
    "DocumentActor",
    "DocumentVersie",
    "DocumentPublicatie",
    "DocumentPublicatieMetadata",
    "Kamerstukdossier",
]
