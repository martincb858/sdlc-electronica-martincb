from sqlalchemy.orm import Session

from app.db import AlertModel


class SqlAlchemyAlertRepository:
    def __init__(self, db_session: Session) -> None:
        self._db = db_session

    def list_for_sensor(self, sensor_id: str) -> list[AlertModel]:
        return (
            self._db.query(AlertModel)
            .filter(AlertModel.sensor_id == sensor_id.upper())
            .order_by(AlertModel.id.asc())
            .all()
        )
