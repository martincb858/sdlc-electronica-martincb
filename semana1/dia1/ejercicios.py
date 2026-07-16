from dataclasses import dataclass
from enum import Enum, auto
from typing import Protocol
 
class SensorType(Enum):            # enums: como tus #define, pero con tipo
    TEMPERATURE = auto()
    HUMIDITY = auto()
 
@dataclass(frozen=True)            # dataclass inmutable: struct + constructor + igualdad
class Reading:
    sensor_id: str
    value: float
    sensor_type: SensorType
 
class Transport(Protocol):         # Protocol: la interfaz sin herencia forzada
    def send(self, payload: bytes) -> None: ...
 
def to_frame(r: Reading) -> bytes: # funcion pura, facil de testear
    return f"{r.sensor_id}:{r.value:.2f}".encode()


# 1. Conversion a Farenheit
def convert_to_farenheit(r: Reading) -> Reading:
    if r.sensor_type == SensorType.TEMPERATURE:
        fahrenheit_val = (r.value * 9/5) + 32
        # Como es frozen=True, no modificamos; retornamos una copia nueva
        return Reading(sensor_id=r.sensor_id, value=round(fahrenheit_val, 2), sensor_type=r.sensor_type)
    return r

# 2. Conversion a Kelvin
def convert_to_kelvin(r: Reading) -> Reading:
    if r.sensor_type == SensorType.TEMPERATURE:
        fahrenheit_val = (r.value  + 273.15)
        return Reading(sensor_id=r.sensor_id, value=round(fahrenheit_val, 2), sensor_type=r.sensor_type)
    return r


# 3. Detección de umbral alto
def is_high(r: Reading, threshold: float) -> bool:
    return r.value > threshold

# 4. Detección de umbral bajo
def is_low(r: Reading, threshold: float) -> bool:
    return r.value < threshold


# 5. Serialización binaria
def to_binary_packet(r: Reading) -> bytes:
    """Serializa la lectura en un formato de bytes compacto [ID_LEN(1B)][ID_STR][TYPE(1B)][VALUE(8B)]"""
    id_bytes = r.sensor_id.encode('utf-8')
    id_len = len(id_bytes).to_bytes(1, byteorder='big')
    type_byte = r.sensor_type.value.to_bytes(1, byteorder='big')
    import struct
    value_bytes = struct.pack('!d', r.value) # '!' para network byte order (big-endian)
    
    return id_len + id_bytes + type_byte + value_bytes

