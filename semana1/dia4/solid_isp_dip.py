from typing import Protocol
from dia3.solid_srp_ocp_lsp import SensorReading
from abc import ABC, abstractmethod

class DataRepository(Protocol):
    def save(self, reading: SensorReading) -> None: ...
    def get_latest(self, sensor_id: str) -> SensorReading | None: ...
 
class DataProcessor:
    """Depende de la abstraccion, no de una implementacion concreta."""
    def __init__(self, repository: DataRepository) -> None:
        self._repo = repository  # inyeccion de dependencias
    def process_and_save(self, reading: SensorReading) -> None:
        # Lógica de procesamiento...
        self._repo.save(reading)
# En produccion: DataProcessor(PostgreSQLRepository())
# En tests:      DataProcessor(InMemoryRepository())  <- sin base de datos


# =====================================================================
# EJEMPLO ISP - INCORRECTO (Mal): Interfaz Gorda
# ====================================================================

class FatSensorInterface_M(ABC):
    """Interfaz que obliga a implementar demasiadas cosas."""
    @abstractmethod
    def read(self) -> SensorReading: ...
    @abstractmethod
    def write(self, config: dict) -> None: ...
    @abstractmethod
    def calibrate(self) -> None: ...
    @abstractmethod
    def reset(self) -> None: ...

class SimpleThermometer_M(FatSensorInterface_M):
    """
    ROMPE ISP: Este es un termómetro súper básico. Solo sabe leer.
    Sin embargo, la interfaz gorda lo OBLIGA a tener los demás métodos.
    """
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id

    def read(self) -> SensorReading:
        return SensorReading(sensor_id=self.sensor_id, value=25.0)

    # Metodos obligatorios que no tienen sentido para este sensor:
    def write(self, config: dict) -> None:
        raise NotImplementedError("Este sensor básico no soporta escritura")

    def calibrate(self) -> None:
        raise NotImplementedError("Este sensor básico no se puede calibrar")

    def reset(self) -> None:
        raise NotImplementedError("Este sensor básico no tiene botón de reset")


# EJEMPLO ISP - CORRECTO (Bien): Interfaces Segregadas
# =====================================================================


# 1. Dividimos el monolito en interfaces pequeñas (como piezas de Lego)
class Readable(ABC):
    @abstractmethod
    def read(self) -> SensorReading: ...

class Writable(ABC):
    @abstractmethod
    def write(self, config: dict) -> None: ...

class Calibratable(ABC):
    @abstractmethod
    def calibrate(self) -> None: ...

# 2. El termómetro simple SOLO hereda lo que necesita
class SimpleThermometer_B(Readable):
    """CUMPLE ISP: Solo hereda Readable, no tiene métodos basura."""
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id

    def read(self) -> SensorReading:
        return SensorReading(sensor_id=self.sensor_id, value=25.0)

# 3. Si mañana llega un sensor avanzado, simplemente hereda varias interfaces
class AdvancedSmartSensor_B(Readable, Writable, Calibratable):
    """CUMPLE ISP: Este sensor sí hace de todo, así que hereda 3 interfaces."""
    def __init__(self, sensor_id: str) -> None:
        self.sensor_id = sensor_id

    def read(self) -> SensorReading:
        return SensorReading(sensor_id=self.sensor_id, value=22.0)

    def write(self, config: dict) -> None:
        pass # Lógica real de escritura

    def calibrate(self) -> None:
        pass # Lógica real de calibración



# =====================================================================
# EJEMPLO DIP - INCORRECTO (Mal): Alto acoplamiento
# =====================================================================

class PostgreSQLRepository_M:
    """Clase de bajo nivel (detalle de implementación)."""
    def save(self, reading: SensorReading) -> None:
        # Simulando una conexión lenta a una base de datos real
        print("Guardando en PostgreSQL...")

class DataProcessor_M:
    """
    ROMPE DIP: La clase de alto nivel instancia directamente a la clase 
    de bajo nivel. Están fuertemente acopladas.
    """
    def __init__(self) -> None:
        # Si queremos testear esto, obligatoriamente intentará conectarse a la DB
        self._repo = PostgreSQLRepository_M()

    def process_and_save(self, reading: SensorReading) -> None:
        # Simula alguna lógica antes de guardar
        reading.value = round(reading.value, 2)
        self._repo.save(reading)


# =====================================================================
# EJEMPLO DIP - CORRECTO (Bien): Inyección de Dependencias y Protocol
# =====================================================================

# 1. Creamos la Abstracción (El contrato)
class DataRepository(Protocol):
    def save(self, reading: SensorReading) -> None: ...
    def get_latest(self, sensor_id: str) -> SensorReading | None: ...

# 2. Detalles de implementación (Clases de bajo nivel)
class PostgreSQLRepository_B:
    """Implementación para Producción."""
    def save(self, reading: SensorReading) -> None:
        print("Guardando en PostgreSQL real...")
        
    def get_latest(self, sensor_id: str) -> SensorReading | None:
        pass # Lógica de DB real

class InMemoryRepository:
    """Implementación para Tests (Simula una base de datos en la RAM)."""
    def __init__(self) -> None:
        self.data: dict[str, SensorReading] = {}

    def save(self, reading: SensorReading) -> None:
        self.data[reading.sensor_id] = reading

    def get_latest(self, sensor_id: str) -> SensorReading | None:
        return self.data.get(sensor_id)

# 3. Clase de alto nivel
class DataProcessor_B:
    """
    CUMPLE DIP: Depende de la abstracción (DataRepository), no de la base de datos real.
    Aceptará CUALQUIER clase que cumpla con el Protocolo.
    """
    def __init__(self, repository: DataRepository) -> None:
        self._repo = repository  # Inyección de dependencia

    def process_and_save(self, reading: SensorReading) -> None:
        reading.value = round(reading.value, 2)
        self._repo.save(reading)