from datetime import datetime, timedelta

import pytest
from src.alert_manager import AlertManager
from src.anomaly_detector import AnomalyDetector
from src.sensor_reading import SensorReading


@pytest.mark.parametrize("temperatura, humedad", [(36.8, 55.0), (37.0, 85.0)])
def test_alert_humedad(temperatura: float, humedad: float, capsys) -> None:
    detector = AnomalyDetector(temp_threshold=35.0, hum_threshold=80.0)
    reading = SensorReading(
        "BODEGA-1", temperatura=temperatura, humedad=humedad, timestamp=datetime.now()
    )

    if detector.evaluate(reading) == "ANOMALIA_HUMEDAD":
        alert_manager = AlertManager()
        alerta = detector.evaluate(reading)
        alert_manager.send_alert(
            reading.device_id, alerta, reading.humedad, reading.timestamp
        )

        consola = capsys.readouterr().out
        assert "ANOMALIA_HUMEDAD" in consola
        assert "BODEGA-1" in consola
        assert str(humedad) in consola
    else:
        pass


def test_alert_throtling(capsys) -> None:
    detector = AnomalyDetector(temp_threshold=35.0, hum_threshold=80.0)
    alert_manager = AlertManager()

    t0 = datetime.now()
    t1 = t0 + timedelta(seconds=30)

    reading_1 = SensorReading(
        "BODEGA-ZONA-1", temperatura=36.5, humedad=60.0, timestamp=t0
    )
    alerta_1 = detector.evaluate(reading_1)

    if alerta_1 == "ANOMALIA_TEMPERATURA":
        alert_manager.send_alert(
            reading_1.device_id, alerta_1, reading_1.temperatura, reading_1.timestamp
        )

        consola_ciclo_1 = capsys.readouterr().out
        assert "ANOMALIA_TEMPERATURA" in consola_ciclo_1
        assert "BODEGA-ZONA-1" in consola_ciclo_1
    else:
        pass

    reading_2 = SensorReading(
        "BODEGA-ZONA-1", temperatura=36.5, humedad=60.0, timestamp=t1
    )
    alerta_2 = detector.evaluate(reading_2)

    if alerta_2 == "ANOMALIA_TEMPERATURA":
        alert_manager.send_alert(
            reading_2.device_id, alerta_2, reading_2.temperatura, reading_2.timestamp
        )

        consola_ciclo_2 = capsys.readouterr().out
        assert consola_ciclo_2 == ""
    else:
        pass
