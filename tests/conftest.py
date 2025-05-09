import os
import pytest
from src.database.sqlite_database import SQLiteDatabase
from src.database.database_config import CURRENT_CONFIG
import time
import sqlite3

@pytest.fixture(scope="function")
def setup_test_database():
    """
    Configura y limpia la base de datos de prueba antes y después de cada prueba.
    """
    # Configurar entorno de prueba
    os.environ['APP_ENV'] = 'testing'
    db_path = CURRENT_CONFIG['test_db_path']

    # Crear instancia de base de datos de prueba
    db = SQLiteDatabase(db_path)
    db.connect()

    # Crear tablas
    db.create_tables()

    yield db

    # Limpiar después de la prueba
    try:
        db.cursor.execute('DELETE FROM productos')
        db.cursor.execute('DELETE FROM ventas')
        db.cursor.execute('DELETE FROM detalle_ventas')
        db.cursor.execute('DELETE FROM usuarios')
        db.conn.commit()
    except:
        pass

    db.disconnect()

@pytest.fixture
def db(setup_test_database):
    """
    Proporciona una instancia de la base de datos para las pruebas.
    """
    return setup_test_database

@pytest.fixture
def inventario_limpio(db):
    """
    Crea y devuelve una instancia limpia de Inventario para las pruebas.
    """
    from src.modelos.inventario import Inventario
    return Inventario(db)

@pytest.fixture
def gestor_usuarios_limpio(db):
    """
    Crea y devuelve una instancia limpia de GestorUsuarios para las pruebas.
    """
    from src.modulos.gestor_usuarios import GestorUsuarios
    return GestorUsuarios(db)
