import os
import sys

# Agregar el directorio src al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from web.app import app
from database.postgres_database import PostgresDatabase
from database.database_config import CURRENT_CONFIG

def inicializar_base_datos():
    """Inicializa la base de datos y crea las tablas necesarias."""
    db = PostgresDatabase(CURRENT_CONFIG)
    db.connect()
    db.create_tables()
    return db

if __name__ == '__main__':
    # Inicializar base de datos
    db = inicializar_base_datos()
    
    # Iniciar la aplicación web
    app.run(debug=True)

#python web_main.py ejecutar este comando directamente en consola 