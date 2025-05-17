import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env si existe
load_dotenv()

# ===============================
# Configuración de PostgreSQL
# ===============================
# Este diccionario almacena los parámetros de conexión a la base de datos PostgreSQL.
# Los valores pueden ser sobreescritos por variables de entorno.
POSTGRES_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': os.getenv('DB_NAME', 'gestor_inventario'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres'),
    'port': os.getenv('DB_PORT', '5432')
}

# ===============================
# Configuración actual del sistema
# ===============================
# Se puede cambiar fácilmente a otra configuración si se soportan otros motores.
CURRENT_CONFIG = POSTGRES_CONFIG 