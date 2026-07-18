from pathlib import Path

import pytest
import json
from dataclasses import FrozenInstanceError
from config import UartConfig
from device import UartDevice
from parsers import ModbusParser, NMEAParser
from recorder import DataRecorder


# --- Tests de config.py ---
def test_uart_config_invalid_baudrate_raises_error() -> None:
    """Verifica que instanciar UartConfig con un baudrate no estándar levante ValueError."""
    with pytest.raises(ValueError, match="no es estándar"):
        UartConfig(baudrate=1234, parity="N", stop_bits=1, timeout=1.0)
    


def test_uart_config_is_immutable() -> None:
    """Verifica que modificar un atributo de UartConfig levante FrozenInstanceError."""
    config = UartConfig(baudrate=9600, parity="N", stop_bits=1, timeout=1.0)

    with pytest.raises(FrozenInstanceError):
        config.baudrate = 115200


# --- Tests de parsers.py ---
def test_modbus_parser_valid_frame() -> None:
    """Verifica que can_parse devuelva True y parse extraiga los datos correctos de una trama RTU válida."""
    parser = ModbusParser()
    # Trama real: Dirección 0x01, Función 0x03, Registro 0x0000, Cantidad 0x0002
    # El CRC correcto para b'\x01\x03\x00\x00\x00\x02' es 0xC40B (en little endian: b'\x0B\xC4')
    valid_frame = b"\x01\x03\x00\x00\x00\x02\xc4\x0b"

    assert parser.can_parse(valid_frame) is True

    result = parser.parse(valid_frame)
    assert result["protocol"] == "Modbus RTU"
    assert result["address"] == 1
    assert result["function"] == 3
    assert result["payload"] == [0, 0, 0, 2]


def test_nmea_parser_invalid_checksum() -> None:
    """Verifica que can_parse devuelva False si la sentencia NMEA tiene el checksum alterado."""
    parser = NMEAParser()
    # Sentencia válida original: $GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\r\n
    # Le cambiamos el checksum intencionalmente a *99
    invalid_frame = (
        b"$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*99\r\n"
    )

    assert parser.can_parse(invalid_frame) is False

    # También verificamos que intentar parsear levante ValueError
    with pytest.raises(ValueError, match="inválida o corrupta"):
        parser.parse(invalid_frame)


# --- Tests de device.py ---
def test_uart_device_read_not_connected_raises_error() -> None:
    """Verifica que intentar read_and_parse sin llamar a connect() levante RuntimeError."""
    config = UartConfig(baudrate=9600, parity="N", stop_bits=1, timeout=1.0)
    parser = NMEAParser()
    device = UartDevice(config, parser)

    with pytest.raises(RuntimeError, match="no está conectado"):
        device.read_and_parse(
            b"$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\r\n"
        )


# --- Tests de recorder.py ---
def test_data_recorder_writes_json_lines(tmp_path: Path) -> None:
    """Verifica que DataRecorder formatee y guarde correctamente un diccionario en el archivo temporal."""
    # tmp_path es un objeto Path que pytest provee mágicamente para archivos temporales
    file_path = tmp_path / "test_logs.jsonl"
    recorder = DataRecorder(file_path)

    # Grabamos dos líneas para confirmar el formato "lines"
    data1 = {"protocol": "NMEA", "latitude": "4807.038"}
    data2 = {"protocol": "Modbus RTU", "address": 1}

    recorder.record(data1)
    recorder.record(data2)

    # Leemos el archivo real para comprobar qué se guardó
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 2
    assert json.loads(lines[0]) == data1
    assert json.loads(lines[1]) == data2
