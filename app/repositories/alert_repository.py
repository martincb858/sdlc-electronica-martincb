from sqlalchemy.orm import Session

from app.db import AlertModel


class SqlAlchemyAlertRepository:
    def __init__(self, db_session: Session) -> None:
        self._db = db_session

    def list_for_sensor(
        self, sensor_id: str, status: str | None = None
    ) -> list[AlertModel]:
        query = self._db.query(AlertModel).filter(
            AlertModel.sensor_id == sensor_id.upper()
        )
        if status is not None:
            query = query.filter(AlertModel.status == status)
        return query.order_by(AlertModel.id.asc()).all()

    def get_by_id(self, alert_id: int) -> AlertModel | None:
        return self._db.query(AlertModel).filter(AlertModel.id == alert_id).first()

    def count_by_status(self, status: str) -> int:
        return (
            self._db.query(AlertModel).filter(AlertModel.status == status).count()
        )

    def update_status(self, alert_id: int, status: str) -> AlertModel:
        alert = self.get_by_id(alert_id)
        if alert is None:
            raise ValueError(f"Alerta {alert_id} no encontrada.")
        alert.status = status
        self._db.commit()
        self._db.refresh(alert)
        return alert
