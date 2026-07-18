import threading
from typing import Any, Optional

class ThreadSafeCircularBuffer:
    """
    Buffer circular FIFO seguro para concurrencia.
    Si el buffer se llena, los datos más antiguos se sobrescriben.
    """
    
    def __init__(self, size: int) -> None:
        self.size = size
        self.buffer = [None] * size
        self.head = 0  # Donde escribimos
        self.tail = 0  # De donde leemos
        self.count = 0 # Elementos actuales
        self.lock = threading.Lock()

    def push(self, item: Any) -> None:
        """Inserta un elemento. Sobrescribe el más viejo si está lleno."""
        with self.lock:  # Adquiere y libera el cerrojo automáticamente
            self.buffer[self.head] = item
            self.head = (self.head + 1) % self.size
            
            if self.count < self.size:
                self.count += 1
            else:
                # Si está lleno, al empujar la cabeza empujamos también la cola
                self.tail = (self.tail + 1) % self.size

    def pop(self) -> Optional[Any]:
        """Extrae el elemento más antiguo. Retorna None si está vacío."""
        with self.lock:
            if self.count == 0:
                return None
                
            item = self.buffer[self.tail]
            self.tail = (self.tail + 1) % self.size
            self.count -= 1
            return item