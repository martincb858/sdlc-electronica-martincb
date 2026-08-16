from typing import Protocol


class AlertStrategy(Protocol):
    """Abstracción para estrategias de notificación de alertas (OCP)."""

    def notify(self, sensor_id: str, value: float, threshold: float) -> None: ...
