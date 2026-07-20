#!/usr/bin/env python3
"""Regenerate Pydantic models from the live OData $metadata document.

Usage::

    uv run python scripts/generate_models.py

This overwrites modules under ``src/tweedekamer/models/`` (except hand-tuned
helpers if you add them later). Review the diff before committing.
"""

from __future__ import annotations

import re
import urllib.request
from pathlib import Path
from xml.etree import ElementTree as ET

METADATA_URL = "https://gegevensmagazijn.tweedekamer.nl/OData/v4/2.0/$metadata"
NS = {
    "edmx": "http://docs.oasis-open.org/odata/ns/edmx",
    "edm": "http://docs.oasis-open.org/odata/ns/edm",
}
TYPE_MAP = {
    "Edm.Guid": "UUID",
    "Edm.String": "str",
    "Edm.Int32": "int",
    "Edm.Int64": "int",
    "Edm.Boolean": "bool",
    "Edm.Date": "date",
    "Edm.DateTimeOffset": "datetime",
    "Edm.Double": "float",
    "Edm.Decimal": "float",
    "Edm.Binary": "bytes",
}
DOMAIN = {
    "persoon": [
        "Persoon",
        "PersoonContactinformatie",
        "PersoonGeschenk",
        "PersoonLoopbaan",
        "PersoonNevenfunctie",
        "PersoonNevenfunctieInkomsten",
        "PersoonOnderwijs",
        "PersoonReis",
    ],
    "commissie": [
        "Commissie",
        "CommissieContactinformatie",
        "CommissieZetel",
        "CommissieZetelVastPersoon",
        "CommissieZetelVastVacature",
        "CommissieZetelVervangerPersoon",
        "CommissieZetelVervangerVacature",
    ],
    "fractie": [
        "Fractie",
        "FractieZetel",
        "FractieZetelPersoon",
        "FractieZetelVacature",
    ],
    "activiteit": [
        "Activiteit",
        "ActiviteitActor",
        "Agendapunt",
        "Besluit",
        "Stemming",
        "Vergadering",
        "Verslag",
        "Zaal",
        "Reservering",
    ],
    "zaak": ["Zaak", "ZaakActor", "Toezegging", "ToegezegdAan"],
    "document": [
        "Document",
        "DocumentActor",
        "DocumentVersie",
        "DocumentPublicatie",
        "DocumentPublicatieMetadata",
        "Kamerstukdossier",
    ],
}

ROOT = Path(__file__).resolve().parents[1]
MODELS = ROOT / "src" / "tweedekamer" / "models"


def to_snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def py_type(edm: str) -> str:
    return TYPE_MAP.get(edm, "Any")


def fetch_entities() -> dict[str, dict]:
    req = urllib.request.Request(METADATA_URL, headers={"User-Agent": "tweedekamer-modelgen/0.1"})
    xml = urllib.request.urlopen(req, timeout=60).read()
    root = ET.fromstring(xml)
    schema = root.find(".//edm:Schema", NS)
    entities: dict[str, dict] = {}
    for et in schema.findall("edm:EntityType", NS):
        name = et.get("Name")
        props = [
            {"name": p.get("Name"), "type": p.get("Type")}
            for p in et.findall("edm:Property", NS)
        ]
        navs = [
            {"name": n.get("Name"), "type": n.get("Type")}
            for n in et.findall("edm:NavigationProperty", NS)
        ]
        entities[name] = {"props": props, "navs": navs}
    return entities


def gen_class(name: str, entities: dict[str, dict]) -> str:
    info = entities[name]
    lines = [f"class {name}(EntityBase):", f'    """OData entity type ``{name}``."""', ""]
    for p in info["props"]:
        pname = p["name"]
        attr = to_snake(pname)
        typ = py_type(p["type"])
        if pname == "Id":
            lines.append(f'    {attr}: {typ} = Field(alias="{pname}")')
        else:
            lines.append(f'    {attr}: {typ} | None = Field(default=None, alias="{pname}")')
    for n in info["navs"]:
        nname = n["name"]
        ntype = n["type"]
        attr = to_snake(nname)
        if ntype.startswith("Collection("):
            inner = ntype[len("Collection(") : -1].split(".")[-1]
            lines.append(f'    {attr}: list[{inner}] | None = Field(default=None, alias="{nname}")')
        else:
            inner = ntype.split(".")[-1]
            lines.append(f'    {attr}: {inner} | None = Field(default=None, alias="{nname}")')
    return "\n".join(lines) + "\n"


def write_base() -> None:
    (MODELS / "base.py").write_text(
        '''\
"""Base model types for Tweede Kamer OData entities."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class EntityBase(BaseModel):
    """Base class for all OData entity models.

    Field names use Python snake_case; the API uses PascalCase aliases.
    Extra fields from the API are allowed so schema additions do not break clients.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        extra="allow",
        from_attributes=True,
    )

    def get(self, name: str, default: Any = None) -> Any:
        """Get a field by Python attribute name or original PascalCase API name."""
        if hasattr(self, name):
            return getattr(self, name)
        for field_name, field in type(self).model_fields.items():
            if field.alias == name:
                return getattr(self, field_name, default)
        if self.__pydantic_extra__ and name in self.__pydantic_extra__:
            return self.__pydantic_extra__[name]
        return default
'''
    )


def main() -> None:
    entities = fetch_entities()
    MODELS.mkdir(parents=True, exist_ok=True)
    write_base()
    all_names: list[str] = []

    for domain, names in DOMAIN.items():
        referenced: set[str] = set()
        for name in names:
            for nav in entities[name]["navs"]:
                ntype = nav["type"]
                inner = (
                    ntype[len("Collection(") : -1].split(".")[-1]
                    if ntype.startswith("Collection(")
                    else ntype.split(".")[-1]
                )
                if inner not in names:
                    referenced.add(inner)

        parts = [
            f'"""Domain models for {domain} entities."""',
            "from __future__ import annotations",
            "",
            "from datetime import date, datetime",
            "from typing import TYPE_CHECKING",
            "from uuid import UUID",
            "",
            "from pydantic import Field",
            "",
            "from tweedekamer.models.base import EntityBase",
            "",
        ]
        if referenced:
            parts.append("if TYPE_CHECKING:")
            for ref in sorted(referenced):
                ref_domain = next(d for d, ns in DOMAIN.items() if ref in ns)
                parts.append(f"    from tweedekamer.models.{ref_domain} import {ref}  # noqa: F401")
            parts.append("")
        parts.append("")
        for name in names:
            parts.append(gen_class(name, entities))
            parts.append("")
            all_names.append(name)
        (MODELS / f"{domain}.py").write_text("\n".join(parts))

    init = [
        '"""Pydantic models for Tweede Kamer OData entities."""',
        "",
        "from __future__ import annotations",
        "",
        "from tweedekamer.models.base import EntityBase",
    ]
    for domain, names in DOMAIN.items():
        for name in names:
            init.append(f"from tweedekamer.models.{domain} import {name}")
    init += ["", "ENTITY_MODELS: dict[str, type[EntityBase]] = {"]
    for name in all_names:
        init.append(f'    "{name}": {name},')
    init += [
        "}",
        "",
        "_ns = {name: cls for name, cls in ENTITY_MODELS.items()}",
        "for _cls in ENTITY_MODELS.values():",
        "    _cls.model_rebuild(_types_namespace=_ns)",
        "",
        "__all__ = [",
        '    "EntityBase",',
        '    "ENTITY_MODELS",',
    ]
    for name in all_names:
        init.append(f'    "{name}",')
    init.append("]")
    init.append("")
    (MODELS / "__init__.py").write_text("\n".join(init))
    print(f"Wrote {len(all_names)} models under {MODELS}")


if __name__ == "__main__":
    main()
