from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertOut(BaseModel):
    id: int
    sensor_id: str
    value: float
    threshold: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
