import os
import pytest
from src.modulos.gestor_usuarios import GestorUsuarios
from src.modelos.inventario import Inventario

@pytest.fixture(autouse=True)
def limpiar_archivos():
    # Antes de cada prueba
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
    return Inventario()

@pytest.fixture
def gestor_usuarios_limpio():
    return GestorUsuarios("data/usuarios_test.json")