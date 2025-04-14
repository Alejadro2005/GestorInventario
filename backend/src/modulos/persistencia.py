import json
import os

class PersistenciaJSON:
    @staticmethod
    def cargar_datos(ruta: str):
        """Carga datos desde un archivo JSON."""
        if not os.path.exists(ruta):
            return []
        with open(ruta, "r", encoding="utf-8") as archivo:
            try:
                return json.load(archivo)
            except json.JSONDecodeError:
                return []

    @staticmethod
    def guardar_datos(ruta: str, datos):
        """Guarda datos en un archivo JSON."""
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
