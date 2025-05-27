"""
Módulo principal de la aplicación web Flask para el sistema de gestión de inventario.
Configura la aplicación, la base de datos y los blueprints.
"""
import os
import sys
from pathlib import Path

# Agregar el directorio src al PYTHONPATH
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from flask import Flask, g
from dotenv import load_dotenv
from database.postgres_database import PostgresDatabase
from database.database_config import CURRENT_CONFIG
from web.controllers.auth import auth_bp
from web.controllers.main import main_bp
from web.controllers.productos import productos_bp
from web.controllers.usuarios import usuarios_bp
from web.controllers.ventas import ventas_bp
from web.controllers.historial import historial_bp

# Cargar variables de entorno
def cargar_variables_entorno():
    """
    Carga las variables de entorno desde un archivo .env si existe.
    """
    load_dotenv()

cargar_variables_entorno()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'clave_secreta_default')

# Configuración de la base de datos
app.config['DATABASE'] = PostgresDatabase(CURRENT_CONFIG)

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(ventas_bp)
app.register_blueprint(historial_bp)

@app.before_request
def before_request():
    """
    Conectar a la base de datos antes de cada petición HTTP.
    """
    g.db = app.config['DATABASE']
    g.db.connect()

@app.teardown_appcontext
def teardown_db(exception):
    """
    Cerrar la conexión a la base de datos después de cada petición HTTP.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    """
    Punto de entrada principal de la aplicación web.
    Crea las tablas necesarias y ejecuta el servidor Flask en modo debug.
    """
    db = app.config['DATABASE']
    db.connect()
    db.create_tables()
    db.disconnect()
    app.run(debug=True) 