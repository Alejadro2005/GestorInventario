from cli.consoleui import ConsoleUI
from src.database.postgres_database import PostgresDatabase
from src.database.database_config import CURRENT_CONFIG
from src.modelos.inventario import Inventario
from src.modulos.gestor_usuarios import GestorUsuarios

if __name__ == "__main__":
    db = PostgresDatabase(CURRENT_CONFIG)
    db.connect()
    db.create_tables()
    inventario = Inventario(db)
    gestor_usuarios = GestorUsuarios(db)
    app = ConsoleUI(inventario, gestor_usuarios)
    app.ejecutar()