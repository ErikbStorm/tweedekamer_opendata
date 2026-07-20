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
