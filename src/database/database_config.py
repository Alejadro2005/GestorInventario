import os
from dotenv import load_dotenv

# Cargar variables de entorno desde un archivo .env si existe
load_dotenv()

class DatabaseConfig:
    """
    Clase para manejar la configuración de la base de datos.
    
    Esta clase proporciona los parámetros de conexión a la base de datos PostgreSQL.
    Los valores pueden ser sobreescritos por variables de entorno.
    """
    
    def __init__(self):
        self.host = os.getenv('DB_HOST', 'localhost')
        self.database = os.getenv('DB_NAME', 'gestor_inventario')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', 'postgres')
        self.port = os.getenv('DB_PORT', '5432')

    def to_dict(self):
        """
        Convierte la configuración a un diccionario.
        
        Returns:
            dict: Diccionario con los parámetros de conexión
        """
        return {
            'host': self.host,
            'database': self.database,
            'user': self.user,
            'password': self.password,
            'port': self.port
        }

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