from typing import Protocol

from sqlalchemy.orm import Session


class AlertStrategy(Protocol):
    """Abstracción para estrategias de notificación de alertas (OCP)."""

    def notify(self, sensor_id: str, value: float, threshold: float) -> None: ...


class ConsoleAlertStrategy:
    """Estrategia de alerta que imprime en consola."""

    def notify(self, sensor_id: str, value: float, threshold: float) -> None:
        print(
            f"[ALERTA CONSOLA] Sensor '{sensor_id}' superó el umbral: "
            f"valor={value}, umbral={threshold}"
        )


class DatabaseAlertStrategy:
    """Estrategia de alerta para persistencia en base de datos."""

    def __init__(self, db_session: Session) -> None:
        self._db = db_session

    def notify(self, sensor_id: str, value: float, threshold: float) -> None:
        # Aquí se ejecutaría la persistencia en la tabla de auditoría/alertas
        # asegurando que la transacción o llamada sea realizada con la sesión.
        pass
