from database.postgres_database import PostgresDatabase
from database.database_config import CURRENT_CONFIG
from modelos.inventario import Inventario
from modulos.gestor_usuarios import GestorUsuarios
from cli.consoleui import ConsoleUI

def inicializar_base_datos():
    """Inicializa la base de datos PostgreSQL"""
    db = PostgresDatabase()
    db.connect()
    return db

def main():
    # Inicializar la base de datos
    db = inicializar_base_datos()
    
    # Crear instancias de los modelos con la base de datos
    inventario = Inventario(db)
    gestor_usuarios = GestorUsuarios(db)
    
    # Crear y ejecutar la interfaz de consola
    ui = ConsoleUI(inventario, gestor_usuarios)
    ui.ejecutar()

if __name__ == '__main__':
    main() 