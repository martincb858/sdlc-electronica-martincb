from pydantic import BaseModel


class MetricsOut(BaseModel):
    sensors_total: int
    sensors_active: int
    readings_total: int
    alerts_open: int
    alerts_acknowledged: int
    alerts_resolved: int
