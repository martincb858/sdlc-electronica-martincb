# S - Una clase, una responsabilidad: SensorReader lee; DataLogger persiste.
# O - AlertStrategy (ABC) con ConsoleAlert y FileAlert: agregar EmailAlert
#     manana NO toca el codigo existente.
# L - TemperatureSensor y HumiditySensor son intercambiables donde se espera
#     BaseSensor: process_sensor(sensor: BaseSensor) funciona con cualquiera.
 
from abc import ABC, abstractmethod
import json
import os
from dataclasses import dataclass  # <--- IMPORTANTE: Agrega esto

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
# Esta clase rompe el SRP porque tiene dos razones para cambiar:
# 1. Si cambia la forma en que se leen/simulan los sensores (hardware, red, etc.)
# 2. Si cambia el método de almacenamiento (guardar en JSON, base de datos, CSV)
class SensorReader_M:
    def __init__(self, sensor_id: str,  target_dir: str = "."):
        self.sensor_id = sensor_id
        self.target_dir = target_dir

    def read(self) -> SensorReading:
        # Simula la lectura de un sensor
        return SensorReading(sensor_id = self.sensor_id, value=75.0)
    
    def log(self, reading: SensorReading, filename : str) -> None:
        # Simula la persistencia de la lectura
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
#Estas clases cumplen el SRP porque tienen una sola razón para cambiar: SensorReader_B solo lee sensores, y DataLogger solo persiste datos.
class SensorReader_B:
    """Clase que cumple con SRP: solo lee sensores."""
    def __init__(self, sensor_id: str):
        self.sensor_id = sensor_id

    def read(self) -> SensorReading:
        # Simula la lectura de un sensor
        return SensorReading(sensor_id = self.sensor_id, value = 75)
    
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
# 1. Esta clase rompe el principio Abierto/Cerrado
class AnomalyDetector_M:
    def __init__(self, threshold: float) -> None:
        self._threshold = threshold
 
    def check(self, reading: SensorReading, alert_type: str) -> None:
        if reading.value > self._threshold:
            message = f"Anomalia en {reading.sensor_id}"
            
            # Si mañana queremos agregar 'email', tenemos que MODIFICAR este código existente.
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

# 1. Definimos las estrategias base y las existentes (Consola y Archivo)
class ConsoleAlert(AlertStrategy):
    def send(self, message: str) -> None:
        print(f"[Console Alert]: {message}")

class FileAlert(AlertStrategy):
    # 1. Pedimos la ruta del archivo al construir la clase
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
    def send(self, message: str) -> None:
        # 2. Ahora el código está CERRADO a modificaciones; usa la variable dinámica
        with open(self.filepath, "a") as f:
            f.write(f"{message}\n")


# 2. El detector está CERRADO a la modificación. No cambiará si hay nuevas alertas.
class AnomalyDetector_B:
    def __init__(self, alert: AlertStrategy, threshold: float) -> None:
        self._alert = alert
        self._threshold = threshold
 
    def check(self, reading: SensorReading) -> None:
        if reading.value > self._threshold:
            self._alert.send(f"Anomalia en {reading.sensor_id}")


# 3. MAÑANA: Agregamos EmailAlert EXTENDIENDO el código, sin modificar lo anterior.
class EmailAlert(AlertStrategy):
    # 1. Pedimos los datos del correo al construir la clase
    def __init__(self, destination_email: str) -> None:
        self.destination_email = destination_email

    def send(self, message: str) -> None:
        # 2. Cerrado a modificaciones: el correo cambia según el objeto, no según el código
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
        pass # Se asume que retorna los datos del sensor

class TemperatureSensor_M(BaseSensor_M):
    def read(self) -> SensorReading:
        return SensorReading(sensor_id=self.sensor_id, value=25.0)

class HumiditySensor_M(BaseSensor_M):
    def read(self) -> dict:
        # ROMPE LSP: En lugar de devolver un SensorReading, devuelve un diccionario.
        # Cambió las "reglas del juego" del Padre.
        return {"sensor_id": self.sensor_id, "value": 60.0}

def process_sensor_M(sensor: BaseSensor_M) -> None:
    reading = sensor.read()
    # Si 'sensor' es TemperatureSensor_M, esto funciona bien.
    # Pero si 'sensor' es HumiditySensor_M, esto EXPLOTA (AttributeError) 
    # porque los diccionarios no tienen el atributo '.value'.
    # Para arreglarlo tendríamos que hacer un 'if isinstance(...)', lo cual demuestra que rompimos el principio.
    print(f"Procesando lectura: {reading.value} del sensor {reading.sensor_id}")


# ---------------------------------------------------------------------
# EJEMPLO QUE SÍ CUMPLE EL LSP
# ---------------------------------------------------------------------

# 1. Definimos un contrato estricto con una Clase Base Abstracta
class BaseSensor(ABC):
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id
        
    @abstractmethod
    def read(self) -> SensorReading: ...

# 2. Las clases hijas respetan el contrato al pie de la letra
class TemperatureSensor(BaseSensor):
    def read(self) -> SensorReading:
        return SensorReading(sensor_id=self.sensor_id, value=22.5)

class HumiditySensor(BaseSensor):
    def read(self) -> SensorReading:
        return SensorReading(sensor_id=self.sensor_id, value=55.0)

# 3. La función cliente que demuestra el principio
def process_sensor_B(sensor: BaseSensor) -> None:
    # CUMPLE LSP: La función confía ciegamente en la abstracción.
    # Al pasarle 'TemperatureSensor' o 'HumiditySensor', ambas devuelven
    # un 'SensorReading' de forma predecible. Son 100% intercambiables.
    reading = sensor.read()
    print(f"Procesando lectura: {reading.value} del sensor {reading.sensor_id}")