from datetime import datetime, timedelta


class AlertManager:
    def __init__(self) -> None:
        self.throttling_window = timedelta(minutes=5)

        self._last_alert_time: dict[str, datetime] = {}

    def send_alert(self, sensor_id: str, alerta: str, valor: float, 
                   timestamp: datetime) -> None:
        last_time = self._last_alert_time.get(sensor_id)

        if last_time is not None and (timestamp - last_time) < self.throttling_window:
            pass
        else:
            print(
                f"[ALERTA] Nodo {sensor_id}: {alerta} detectada con lectura de {valor}")
            self._last_alert_time[sensor_id] = timestamp