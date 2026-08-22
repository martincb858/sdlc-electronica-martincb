from collections.abc import Sequence

from app.domain.alerts import AlertStrategy


class AnomalyDetectorService:
    """Servicio de dominio para detectar anomalías y disparar alertas."""

    def __init__(
        self,
        alert_strategy: AlertStrategy | Sequence[AlertStrategy],
    ) -> None:
        if isinstance(alert_strategy, Sequence):
            self._alert_strategies: list[AlertStrategy] = list(alert_strategy)
        else:
            self._alert_strategies = [alert_strategy]

    def process_reading(
        self, sensor_id: str, value: float, threshold: float | None
    ) -> None:
        """Evalúa si el valor leído supera el umbral del sensor y notifica."""
        if threshold is None:
            return

        if value > threshold:
            for strategy in self._alert_strategies:
                strategy.notify(sensor_id, value, threshold)
