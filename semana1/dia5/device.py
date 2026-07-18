from typing import Optional, Dict, Any
from config import UartConfig
from parsers import MessageParser


class UartDevice:
    """
    Representa el dispositivo físico UART.
    Recibe su configuración y estrategia de parseo por inyección de dependencias (DIP).
    """

    def __init__(self, config: UartConfig, parser: MessageParser):
        """Inicializa el dispositivo inyectando la configuración y el parser."""
        self.config = config
        self.parser = parser
        self._is_connected = False

    def connect(self) -> None:
        """Abre la conexión serial utilizando los parámetros de self.config."""
        if self._is_connected:
            raise RuntimeError("El dispositivo UART ya se encuentra conectado.")      
        self._is_connected = True


    def disconnect(self) -> None:
        """Cierra la conexión serial de forma segura."""
        if self._is_connected:
            self._is_connected = False


    def read_and_parse(self, raw_data: bytes) -> Optional[Dict[str, Any]]:
        """
        Lee datos del bus y utiliza el parser inyectado para decodificarlos.
        Levanta RuntimeError si el dispositivo no está conectado.
        """
        if not self._is_connected:
            raise RuntimeError("Operación denegada: El dispositivo UART no está conectado.")

        # Delega la validación y el parseo a la abstracción
        if self.parser.can_parse(raw_data):
            return self.parser.parse(raw_data)
        else:
           
            return None