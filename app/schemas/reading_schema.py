from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReadingCreate(BaseModel):
    value: float = Field(..., description="Valor medido por el sensor", examples=[24.5])
    unit: str = Field(default="C", description="Unidad de medida", examples=["C"])

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