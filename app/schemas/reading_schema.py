from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.validator import ValidatorRegistry, physics_registry


class ReadingCreate(BaseModel):
    value: float = Field(..., description="Valor medido por el sensor", examples=[24.5])
    unit: str = Field(default="C", description="Unidad de medida", examples=["C"])

    _physics_registry: ValidatorRegistry = physics_registry

    @model_validator(mode="after")
    def validate_physics(self) -> "ReadingCreate":
        unit = self.unit.upper()
        validator = self._physics_registry.get(unit)
        validator.validate(self.value)
        self.unit = unit
        return self


class ReadingUpdate(BaseModel):
    value: float | None = Field(default=None, examples=[25.1])
    unit: str | None = Field(default=None, examples=["C"])


class ReadingOut(BaseModel):
    id: int
    sensor_id: str
    value: float
    unit: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)