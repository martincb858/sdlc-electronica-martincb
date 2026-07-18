from abc import ABC, abstractmethod
from typing import Dict, Any

class MessageParser(ABC):
    """
    Interfaz abstracta para los parsers de mensajes UART.
    """
    
    @abstractmethod
    def can_parse(self, data: bytes) -> bool:
        """Determina si la trama de bytes corresponde a este protocolo."""
        pass

    @abstractmethod
    def parse(self, data: bytes) -> Dict[str, Any]:
        """Extrae la información de la trama y la retorna como un diccionario."""
        pass


class ModbusParser(MessageParser):
    """Implementación de MessageParser para tramas Modbus RTU."""
    

    def _calculate_crc(self, data: bytes) -> int:
        """Calcula el CRC-16 utilizado en Modbus RTU."""
        crc = 0xFFFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if (crc & 0x0001) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        return crc
    
    def can_parse(self, data: bytes) -> bool:
        """Verifica longitud mínima y CRC válido para Modbus RTU."""
        if len(data) < 4:
            return False
            
        payload = data[:-2]
        received_crc = int.from_bytes(data[-2:], byteorder='little')
        expected_crc = self._calculate_crc(payload)
        
        return expected_crc == received_crc

    def parse(self, data: bytes) -> Dict[str, Any]:
        """Extrae la dirección, función y payload de la trama Modbus."""
        if not self.can_parse(data):
            raise ValueError("Trama Modbus RTU inválida o corrupta")
            
        return {
            "protocol": "Modbus RTU",
            "address": data[0],
            "function": data[1],
            "payload": list(data[2:-2])
        }


class NMEAParser(MessageParser):
    """Implementación de MessageParser para sentencias NMEA (ej. $GPGGA)."""
    
    def can_parse(self, data: bytes) -> bool:
        """Verifica que empiece con '$', termine con '\\r\\n' y tenga un checksum válido."""
        try:
            text = data.decode('ascii')
            if not (text.startswith('$') and text.endswith('\r\n')):
                return False
                
            if '*' not in text:
                return False
                
            # Separar el contenido del checksum
            body, checksum_str = text[1:].rsplit('*', 1)
            checksum_str = checksum_str.strip()  # Quitar el \r\n
            
            # El checksum NMEA es un XOR de todos los caracteres entre '$' y '*'
            calculated_checksum = 0
            for char in body:
                calculated_checksum ^= ord(char)
                
            return int(checksum_str, 16) == calculated_checksum
            
        except (UnicodeDecodeError, ValueError):
            return False

    def parse(self, data: bytes) -> Dict[str, Any]:
        """Extrae latitud, longitud y calidad de la señal de la sentencia $GPGGA."""
        if not self.can_parse(data):
            raise ValueError("Sentencia NMEA inválida o corrupta")
            
        text = data.decode('ascii').strip()
        parts = text.split(',')
        
        # Estructura base. Si no es GPGGA, devolvemos un diccionario genérico.
        result: Dict[str, Any] = {
            "protocol": "NMEA",
            "type": parts[0].replace('$', '')
        }
        
        if result["type"] == "GPGGA":
            result.update({
                "time": parts[1] if len(parts) > 1 else "",
                "latitude": parts[2] if len(parts) > 2 else "",
                "lat_dir": parts[3] if len(parts) > 3 else "",
                "longitude": parts[4] if len(parts) > 4 else "",
                "lon_dir": parts[5] if len(parts) > 5 else "",
                "quality": int(parts[6]) if len(parts) > 6 and parts[6].isdigit() else 0
            })
            
        return result

class CanParser(MessageParser):
    """
    Implementación de MessageParser para tramas CAN simplificadas.
    Estructura asumida: ID (2 bytes) + DLC (1 byte) + Payload (DLC bytes).
    """
    
    def can_parse(self, data: bytes) -> bool:
        """Verifica que la longitud total coincida con el campo DLC."""
        if len(data) < 3:
            return False
            
        dlc = data[2]
        # La trama total debe ser exactamente 3 bytes de cabecera + los bytes del payload
        return len(data) == (3 + dlc)

    def parse(self, data: bytes) -> Dict[str, Any]:
        """Extrae el ID del nodo, el tamaño y los datos del payload."""
        if not self.can_parse(data):
            raise ValueError("Trama CAN inválida o longitud incorrecta")
            
        can_id = int.from_bytes(data[0:2], byteorder='big')
        dlc = data[2]
        
        return {
            "protocol": "CAN",
            "node_id": hex(can_id),
            "dlc": dlc,
            "payload": list(data[3:3+dlc])
        }