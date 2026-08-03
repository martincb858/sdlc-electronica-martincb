from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.domain.sensor_types import sensor_type_registry


class SensorCreate(BaseModel):
    code: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Identificador único del sensor",
        examples=["TEMP-01"],
    )
    name: str = Field(..., min_length=1, examples=["Sensor de sala A"])
    sensor_type: str = Field(
        ...,
        description="Tipo de sensor (determina qué unidades acepta)",
        examples=["TEMPERATURE"],
    )
    location: str | None = Field(default=None, examples=["Sala A"])

    @field_validator("code")
    @classmethod
    def normalize_code(cls, v: str) -> str:
        return v.strip().upper()

    @field_validator("sensor_type")
    @classmethod
    def validate_sensor_type(cls, v: str) -> str:
        sensor_type_registry.get(v)  # ValueError si el tipo no está registrado
        return v.upper()


class SensorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    location: str | None = Field(default=None)


class SensorOut(BaseModel):
    id: int
    code: str
    name: str
    sensor_type: str
    location: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
