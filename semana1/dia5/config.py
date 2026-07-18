from dataclasses import dataclass


@dataclass(frozen=True)
class UartConfig:
    """
    Configuración inmutable para la comunicación UART.
    Aplica el principio SRP al aislar los parámetros de configuración.
    """

    baudrate: int
    parity: str
    stop_bits: int
    timeout: float

    def __post_init__(self) -> None:
        """
        Valida los parámetros de configuración una vez instanciados.
        Debe levantar ValueError si el baudrate no es estándar (ej. 9600, 115200)
        o si los valores de paridad o stop_bits son inválidos.
        """
        valid_baudrates = {9600, 19200, 38400, 57600, 115200}
        valid_parities = {"N", "E", "O"}  # None, Even, Odd
        valid_stop_bits = {1, 2}
        if self.baudrate not in valid_baudrates:
            raise ValueError(f"Baudrate {self.baudrate} no es estándar.")

        if self.parity not in valid_parities:
            raise ValueError(f"Paridad '{self.parity}' inválida.")

        if self.stop_bits not in valid_stop_bits:
            raise ValueError(f"Stop bits {self.stop_bits} inválidos.")
