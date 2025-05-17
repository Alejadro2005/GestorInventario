
import os
import json

def ruta_absoluta(relativa: str) -> str:
    """
    Devuelve la ruta absoluta a partir de un path relativo al proyecto.

    Args:
        relativa (str): El path relativo desde el directorio actual.

    Returns:
        str: La ruta absoluta generada a partir del path relativo.
    """
    raiz = os.path.dirname(os.path.dirname(__file__))  # Sube dos niveles desde este archivo
    return os.path.join(raiz, relativa)

class PersistenciaJSON:
    @staticmethod
    def cargar_datos(ruta: str):
        """
        Carga datos desde un archivo JSON.

        Args:
            ruta (str): La ruta del archivo JSON desde el cual se cargarán los datos.

        Returns:
            list: Una lista con los datos cargados desde el archivo JSON. Si ocurre un error
                  o el archivo no existe, retorna una lista vacía.
        """
        if not os.path.exists(ruta):
            return []
        with open(ruta, "r", encoding="utf-8") as archivo:
            try:
                return json.load(archivo)
            except json.JSONDecodeError:
                return []

    @staticmethod
    def guardar_datos(ruta: str, datos):
        """
        Guarda datos en un archivo JSON.

        Args:
            ruta (str): La ruta del archivo donde se guardarán los datos.
            datos (list): Los datos que se guardarán en el archivo JSON.

        Returns:
            None
        """
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

