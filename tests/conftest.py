import pytest
from src.database.test_database import DatabaseTest
from src.modelos.inventario import Inventario

@pytest.fixture
def inventario_limpio():
    db = DatabaseTest()
    db.connect()
    db.create_tables()
    yield Inventario(db)
    db.disconnect()