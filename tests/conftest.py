import os
import pytest
from src.modulos.gestor_usuarios import GestorUsuarios
from src.modelos.inventario import Inventario

@pytest.fixture(autouse=True)
def limpiar_archivos():
    """
    Elimina los archivos de ventas y usuarios de prueba antes y después de cada prueba.

    Esta función fixture es ejecutada automáticamente antes de cada prueba debido a
    la opción `autouse=True`. Se asegura de que los archivos de datos de prueba
    estén limpios antes de las pruebas y que se eliminen después de que cada prueba termine.

    Archivos que se eliminan:
        - data/ventas.json
        - data/usuarios_test.json
    """
    archivos = ["data/ventas.json", "data/usuarios_test.json"]
    for archivo in archivos:
        if os.path.exists(archivo):
            os.remove(archivo)
    yield
    # Después de cada prueba
    for archivo in archivos:
        if os.path.exists(archivo):
            os.remove(archivo)

@pytest.fixture
def inventario_limpio():
    """
    Crea y devuelve una instancia limpia de Inventario para las pruebas.

    Esta fixture permite que cada prueba tenga un inventario limpio y separado de otras pruebas.

    Returns:
        Inventario: Una nueva instancia de la clase Inventario.
    """
    return Inventario()

@pytest.fixture
def gestor_usuarios_limpio():
    """
    Crea y devuelve una instancia limpia de GestorUsuarios para las pruebas.

    Esta fixture permite que cada prueba tenga un gestor de usuarios limpio y separado de otras pruebas.

    Returns:
        GestorUsuarios: Una nueva instancia de la clase GestorUsuarios, utilizando un archivo de usuarios de prueba.
    """
    return GestorUsuarios("data/usuarios_test.json")
