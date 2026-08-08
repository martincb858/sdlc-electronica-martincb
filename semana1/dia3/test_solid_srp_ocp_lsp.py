import json
import os

import pytest
from solid_srp_ocp_lsp import (
    AlertStrategy,
    AnomalyDetector_B,
    AnomalyDetector_M,
    BaseSensor,
    ConsoleAlert,
    DataLogger,
    FileAlert,
    HumiditySensor,
    HumiditySensor_M,
    SensorReader_B,
    SensorReader_M,
    SensorReading,
    TemperatureSensor,
    TemperatureSensor_M,
    process_sensor_B,
    process_sensor_M,
)

# =====================================================================
# EJEMPLOS SRP
# =====================================================================


def test_SRP_M() -> None:

    filename = "test_sensor_log.json"
    reader = SensorReader_M(sensor_id="TEMP-01", target_dir=".")

    # Probar lectura
    reading = reader.read()
    assert isinstance(reading, SensorReading)
    assert reading.sensor_id == "TEMP-01"
    assert reading.value == 75.0

    # Probar log
    reader.log(reading, "test_sensor_log.json")
    assert os.path.exists(filename)

    with open(filename) as f:
        saved_data = json.load(f)

    assert saved_data["sensor_id"] == "TEMP-01"
    assert saved_data["value"] == 75.0

    # Borrar archivo de prueba
    if os.path.exists(filename):
        os.remove(filename)


def test_SRP_B() -> None:

    filename = "test_sensor_log.json"
    reader = SensorReader_B(sensor_id="TEMP-01")
    logger = DataLogger(target_dir=".")

    # Probar lectura
    reading = reader.read()
    assert isinstance(reading, SensorReading)
    assert reading.sensor_id == "TEMP-01"
    assert reading.value == 75.0

    # Probar log
    logger.log(reading, "test_sensor_log.json")
    assert os.path.exists(filename)

    with open(filename) as f:
        saved_data = json.load(f)

    assert saved_data["sensor_id"] == "TEMP-01"
    assert saved_data["value"] == 75.0

    # Borrar archivo de prueba
    if os.path.exists(filename):
        os.remove(filename)


# =====================================================================
# TEST OCP OCP
# =====================================================================


@pytest.mark.parametrize("value", [75.0, 65.0])
@pytest.mark.parametrize("alert_type", ["console", "file", "email"])
def test_OCP_M(value: float, alert_type: str) -> None:

    detector = AnomalyDetector_M(threshold=70.0)
    reading = SensorReading(sensor_id="TEMP-01", value=value)

    if alert_type == "email" and value > 70.0:
        with pytest.raises(ValueError) as exc_info:
            detector.check(reading, alert_type=alert_type)
        assert str(exc_info.value) == "Tipo de alerta no soportado"

    else:
        detector.check(reading, alert_type=alert_type)


@pytest.mark.parametrize("value", [75.0, 65.0])
@pytest.mark.parametrize(
    "strategy", [ConsoleAlert(), FileAlert(filepath="test_alerts.log")]
)
def test_OCP_B(
    strategy: AlertStrategy, value: float, capsys: pytest.CaptureFixture
) -> None:

    detector = AnomalyDetector_B(alert=strategy, threshold=70.0)
    reading = SensorReading(sensor_id="TEMP-01", value=value)
    expected_message = "Anomalia en TEMP-01"

    if isinstance(strategy, FileAlert) and os.path.exists(strategy.filepath):
        os.remove(strategy.filepath)

    detector.check(reading)

    if value > 70.0:
        if isinstance(strategy, ConsoleAlert):
            captured = capsys.readouterr()
            assert expected_message in captured.out

        elif isinstance(strategy, FileAlert):
            assert os.path.exists(strategy.filepath)
            with open(strategy.filepath) as f:
                assert expected_message in f.read()

            os.remove(strategy.filepath)

    else:
        if isinstance(strategy, ConsoleAlert):
            captured = capsys.readouterr()
            assert expected_message not in captured.out

        elif isinstance(strategy, FileAlert):
            # El archivo no debería haberse creado
            assert not os.path.exists(strategy.filepath)


# =====================================================================
# TEST OCP LSP
# =====================================================================


def test_LSP_M() -> None:
    """Demuestra cómo HumiditySensor_M rompe la sustitución de Liskov."""

    sensor_temp = TemperatureSensor_M(sensor_id="TEMP-01")
    sensor_hum = HumiditySensor_M(sensor_id="HUM-01")

    process_sensor_M(sensor_temp)

    with pytest.raises(AttributeError) as exc_info:
        process_sensor_M(sensor_hum)

    assert "'dict' object has no attribute 'value'" in str(exc_info.value)


@pytest.mark.parametrize(
    "sensor_instance, expected_value",
    [
        (TemperatureSensor(sensor_id="TEMP-01"), 22.5),
        (HumiditySensor(sensor_id="HUM-01"), 55.0),
    ],
)
def test_LSP_B(
    sensor_instance: BaseSensor, expected_value: float, capsys: pytest.CaptureFixture
) -> None:

    process_sensor_B(sensor_instance)

    captured = capsys.readouterr()
    expected_message = f"Lectura: {expected_value} sensor {sensor_instance.sensor_id}"

    assert expected_message in captured.out
