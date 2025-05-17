from gui.app import TiendaApp
from src.database.postgres_database import PostgresDatabase
from src.database.database_config import CURRENT_CONFIG

def inicializar_base_datos():
    """Inicializa la base de datos y crea las tablas necesarias."""
    db = PostgresDatabase(CURRENT_CONFIG)
    db.connect()
    db.create_tables()
    return db

if __name__ == '__main__':
    # Inicializar base de datos
    db = inicializar_base_datos()
    
    # Iniciar la aplicación
    app = TiendaApp(db)
    app.run()

#python gui_main.py ejecutar este comando directamente en consola