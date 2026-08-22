from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AlertOut(BaseModel):
    id: int
    sensor_id: str
    value: float
    threshold: float
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class AlertStatusUpdate(BaseModel):
    status: str = Field(..., examples=["acknowledged"])
