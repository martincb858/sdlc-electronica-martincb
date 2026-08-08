import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest
from config import UartConfig
from device import UartDevice
from parsers import ModbusParser, NMEAParser
from recorder import DataRecorder


# --- Tests de config.py ---
def test_uart_config_invalid_baudrate_raises_error() -> None:
    with pytest.raises(ValueError, match="no es estándar"):
        UartConfig(baudrate=1234, parity="N", stop_bits=1, timeout=1.0)
    


def test_uart_config_is_immutable() -> None:

    config = UartConfig(baudrate=9600, parity="N", stop_bits=1, timeout=1.0)

    with pytest.raises(FrozenInstanceError):
        config.baudrate = 115200


# --- Tests de parsers.py ---
def test_modbus_parser_valid_frame() -> None:

    parser = ModbusParser()

    valid_frame = b"\x01\x03\x00\x00\x00\x02\xc4\x0b"

    assert parser.can_parse(valid_frame) is True

    result = parser.parse(valid_frame)
    assert result["protocol"] == "Modbus RTU"
    assert result["address"] == 1
    assert result["function"] == 3
    assert result["payload"] == [0, 0, 0, 2]


def test_nmea_parser_invalid_checksum() -> None:

    parser = NMEAParser()

    invalid_frame = (
        b"$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*99\r\n"
    )

    assert parser.can_parse(invalid_frame) is False

    with pytest.raises(ValueError, match="inválida o corrupta"):
        parser.parse(invalid_frame)


# --- Tests de device.py ---
def test_uart_device_read_not_connected_raises_error() -> None:

    config = UartConfig(baudrate=9600, parity="N", stop_bits=1, timeout=1.0)
    parser = NMEAParser()
    device = UartDevice(config, parser)

    with pytest.raises(RuntimeError, match="no está conectado"):
        device.read_and_parse(
            b"$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47\r\n"
        )


# --- Tests de recorder.py ---
def test_data_recorder_writes_json_lines(tmp_path: Path) -> None:

    file_path = tmp_path / "test_logs.jsonl"
    recorder = DataRecorder(file_path)


    data1 = {"protocol": "NMEA", "latitude": "4807.038"}
    data2 = {"protocol": "Modbus RTU", "address": 1}

    recorder.record(data1)
    recorder.record(data2)


    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 2
    assert json.loads(lines[0]) == data1
    assert json.loads(lines[1]) == data2
