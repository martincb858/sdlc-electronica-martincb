from app.domain.alerts import AlertStrategy


class AnomalyDetectorService:
    def __init__(
        self,
        alert_strategy: AlertStrategy,
        thresholds: dict[str, float] | None = None,
    ) -> None:
        self._alert_strategy = alert_strategy
        self._thresholds = thresholds or {}

    def process_reading(self, sensor_id: str, value: float) -> None:
        """Procesa una lectura y evalúa si supera el umbral configurado.

        Fase RED: La lógica aún no está implementada para permitir que las pruebas fallen.
        """
        pass
