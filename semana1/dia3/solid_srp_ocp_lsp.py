# S - Una clase, una responsabilidad: SensorReader lee; DataLogger persiste.
# O - AlertStrategy (ABC) con ConsoleAlert y FileAlert: agregar EmailAlert
#     manana NO toca el codigo existente.
# L - TemperatureSensor y HumiditySensor son intercambiables donde se espera
#     BaseSensor: process_sensor(sensor: BaseSensor) funciona con cualquiera.

import json
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class SensorReading:
    sensor_id: str
    value: float


class AlertStrategy(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...


class AnomalyDetector:
    def __init__(self, alert: AlertStrategy, threshold: float) -> None:
        self._alert = alert
        self._threshold = threshold

    def check(self, reading: SensorReading) -> None:
        if reading.value > self._threshold:
            self._alert.send(f"Anomalia en {reading.sensor_id}")


# =====================================================================
# EJEMPLOS SRP
# =====================================================================


# ---------------------------------------------------------------------
# EJEMPLO QUE NO CUMPLE EL SRP
# ---------------------------------------------------------------------


class SensorReader_M:
    def __init__(self, sensor_id: str, target_dir: str = "."):
        self.sensor_id = sensor_id
        self.target_dir = target_dir

    def read(self) -> SensorReading:

        return SensorReading(sensor_id=self.sensor_id, value=75.0)

    def log(self, reading: SensorReading, filename: str) -> None:

        filepath = os.path.join(self.target_dir, filename)
        data = {
            "sensor_id": reading.sensor_id,
            "value": reading.value,
        }
        with open(filepath, "w") as f:
            json.dump(data, f)


# ---------------------------------------------------------------------
# EJEMPLO QUE CUMPLE EL SRP
# ---------------------------------------------------------------------


class SensorReader_B:
    """Clase que cumple con SRP: solo lee sensores."""

    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id

    def read(self) -> SensorReading:
        # Simula la lectura de un sensor
        return SensorReading(sensor_id=self.sensor_id, value=75)


class DataLogger:
    """Se encarga ÚNICAMENTE de la persistencia de los datos en disco."""

    def __init__(self, target_dir: str = "."):
        self.target_dir = target_dir

    def log(self, reading: SensorReading, filename: str) -> None:
        filepath = os.path.join(self.target_dir, filename)
        data = {
            "sensor_id": reading.sensor_id,
            "value": reading.value,
        }
        with open(filepath, "w") as f:
            json.dump(data, f)


# =====================================================================
# EJEMPLOS OCP
# =====================================================================

# ---------------------------------------------------------------------
# EJEMPLO QUE NO CUMPLE EL OCP
# ---------------------------------------------------------------------


class AnomalyDetector_M:
    def __init__(self, threshold: float) -> None:
        self._threshold = threshold

    def check(self, reading: SensorReading, alert_type: str) -> None:
        if reading.value > self._threshold:
            message = f"Anomalia en {reading.sensor_id}"

            if alert_type == "console":
                print(f"[Console Alert]: {message}")
            elif alert_type == "file":
                with open("alerts.log", "a") as f:
                    f.write(f"{message}\n")
            else:
                raise ValueError("Tipo de alerta no soportado")


# ---------------------------------------------------------------------
# EJEMPLO QUE CUMPLE EL OCP
# ---------------------------------------------------------------------


class ConsoleAlert(AlertStrategy):
    def send(self, message: str) -> None:
        print(f"[Console Alert]: {message}")


class FileAlert(AlertStrategy):
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    def send(self, message: str) -> None:

        with open(self.filepath, "a") as f:
            f.write(f"{message}\n")


class AnomalyDetector_B:
    def __init__(self, alert: AlertStrategy, threshold: float) -> None:
        self._alert = alert
        self._threshold = threshold

    def check(self, reading: SensorReading) -> None:
        if reading.value > self._threshold:
            self._alert.send(f"Anomalia en {reading.sensor_id}")


class EmailAlert(AlertStrategy):
    def __init__(self, destination_email: str) -> None:
        self.destination_email = destination_email

    def send(self, message: str) -> None:

        print(f"[Email Alert]: Enviando a {self.destination_email} -> {message}")


# =====================================================================
# EJEMPLOS LSP (Liskov Substitution Principle)
# =====================================================================


# ---------------------------------------------------------------------
# EJEMPLO QUE NO CUMPLE EL LSP
# ---------------------------------------------------------------------
class BaseSensor_M:
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id

    def read(self):
        pass


class TemperatureSensor_M(BaseSensor_M):
    def read(self) -> SensorReading:
        return SensorReading(sensor_id=self.sensor_id, value=25.0)


class HumiditySensor_M(BaseSensor_M):
    def read(self) -> dict:

        return {"sensor_id": self.sensor_id, "value": 60.0}


def process_sensor_M(sensor: BaseSensor_M) -> None:
    reading = sensor.read()
    print(f"Procesando lectura: {reading.value} del sensor {reading.sensor_id}")


# ---------------------------------------------------------------------
# EJEMPLO QUE SÍ CUMPLE EL LSP
# ---------------------------------------------------------------------


class BaseSensor(ABC):
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id

    @abstractmethod
    def read(self) -> SensorReading: ...


class TemperatureSensor(BaseSensor):
    def read(self) -> SensorReading:
        return SensorReading(sensor_id=self.sensor_id, value=22.5)


class HumiditySensor(BaseSensor):
    def read(self) -> SensorReading:
        return SensorReading(sensor_id=self.sensor_id, value=55.0)


def process_sensor_B(sensor: BaseSensor) -> None:

    reading = sensor.read()
    print(f"Procesando lectura: {reading.value} del sensor {reading.sensor_id}")
