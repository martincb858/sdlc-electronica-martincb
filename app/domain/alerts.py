from typing import Protocol

from sqlalchemy.orm import Session

from app.db import AlertModel


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
        alert = AlertModel(
            sensor_id=sensor_id,
            value=value,
            threshold=threshold,
        )
        self._db.add(alert)
        self._db.commit()
        self._db.refresh(alert)
