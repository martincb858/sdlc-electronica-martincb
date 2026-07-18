import json
from typing import Dict, Any
from pathlib import Path


class DataRecorder:
    """
    Responsable exclusivamente de persistir datos en formato JSON-lines.
    """

    def __init__(self, filepath: str | Path) -> None:
        """Configura la ruta del archivo de destino."""
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def record(self, data: Dict[str, Any]) -> None :
        """
        Agrega un diccionario como una nueva línea JSON en el archivo.
        Debe abrir el archivo en modo 'append' (a).
        """
        with open(self.filepath, mode="a", encoding="utf-8") as f:
            # json.dumps serializa el diccionario en un string en formato JSON
            json_line = json.dumps(data)
            f.write(json_line + "\n")
