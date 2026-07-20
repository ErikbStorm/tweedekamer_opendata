# Entities

The OData service exposes **38 entity sets**. Models are defined under `tweedekamer.models` and mirror the live `$metadata` schema.

Official overview: [Informatiemodel](https://opendata.tweedekamer.nl/documentatie/informatiemodel).

## Person / actors

| Entity set | Client accessor | Model |
| --- | --- | --- |
| Persoon | `client.personen` | `Persoon` |
| PersoonContactinformatie | `client.persoon_contactinformatie` | `PersoonContactinformatie` |
| PersoonGeschenk | `client.persoon_geschenken` | `PersoonGeschenk` |
| PersoonLoopbaan | `client.persoon_loopbanen` | `PersoonLoopbaan` |
| PersoonNevenfunctie | `client.persoon_nevenfuncties` | `PersoonNevenfunctie` |
| PersoonNevenfunctieInkomsten | `client.persoon_nevenfunctie_inkomsten` | `PersoonNevenfunctieInkomsten` |
| PersoonOnderwijs | `client.persoon_onderwijs` | `PersoonOnderwijs` |
| PersoonReis | `client.persoon_reizen` | `PersoonReis` |

## Fracties

| Entity set | Client accessor | Model |
| --- | --- | --- |
| Fractie | `client.fracties` | `Fractie` |
| FractieZetel | `client.fractie_zetels` | `FractieZetel` |
| FractieZetelPersoon | `client.fractie_zetel_personen` | `FractieZetelPersoon` |
| FractieZetelVacature | `client.fractie_zetel_vacatures` | `FractieZetelVacature` |

## Commissies

| Entity set | Client accessor | Model |
| --- | --- | --- |
| Commissie | `client.commissies` | `Commissie` |
| CommissieContactinformatie | `client.commissie_contactinformatie` | `CommissieContactinformatie` |
| CommissieZetel | `client.commissie_zetels` | `CommissieZetel` |
| CommissieZetelVastPersoon | `client.commissie_zetel_vast_personen` | `CommissieZetelVastPersoon` |
| CommissieZetelVastVacature | `client.commissie_zetel_vast_vacatures` | `CommissieZetelVastVacature` |
| CommissieZetelVervangerPersoon | `client.commissie_zetel_vervanger_personen` | `CommissieZetelVervangerPersoon` |
| CommissieZetelVervangerVacature | `client.commissie_zetel_vervanger_vacatures` | `CommissieZetelVervangerVacature` |

## Parliamentary process

| Entity set | Client accessor | Model |
| --- | --- | --- |
| Activiteit | `client.activiteiten` | `Activiteit` |
| ActiviteitActor | `client.activiteit_actors` | `ActiviteitActor` |
| Agendapunt | `client.agendapunten` | `Agendapunt` |
| Besluit | `client.besluiten` | `Besluit` |
| Stemming | `client.stemmingen` | `Stemming` |
| Vergadering | `client.vergaderingen` | `Vergadering` |
| Verslag | `client.verslagen` | `Verslag` |
| Zaal | `client.zalen` | `Zaal` |
| Reservering | `client.reserveringen` | `Reservering` |
| Zaak | `client.zaken` | `Zaak` |
| ZaakActor | `client.zaak_actors` | `ZaakActor` |
| Toezegging | `client.toezeggingen` | `Toezegging` |
| ToegezegdAan | `client.toegezegd_aan` | `ToegezegdAan` |

## Documents

| Entity set | Client accessor | Model |
| --- | --- | --- |
| Document | `client.documenten` | `Document` |
| DocumentActor | `client.document_actors` | `DocumentActor` |
| DocumentVersie | `client.document_versies` | `DocumentVersie` |
| DocumentPublicatie | `client.document_publicaties` | `DocumentPublicatie` |
| DocumentPublicatieMetadata | `client.document_publicatie_metadata` | `DocumentPublicatieMetadata` |
| Kamerstukdossier | `client.kamerstukdossiers` | `Kamerstukdossier` |

## Registry

All models are registered in `ENTITY_MODELS`:

```python
from tweedekamer.models import ENTITY_MODELS, Zaak

assert ENTITY_MODELS["Zaak"] is Zaak
```
