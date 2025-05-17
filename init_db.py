import os
import psycopg2
from dotenv import load_dotenv

def init_database():
    """Inicializa la base de datos con las tablas y datos iniciales."""
    # Cargar variables de entorno
    load_dotenv()
    
    # Obtener configuración de la base de datos
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'gestor_inventario'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'alejo123')
    }
    
    try:
        # Conectar a PostgreSQL
        conn = psycopg2.connect(**db_config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Conectado a PostgreSQL")
        
        # Leer y ejecutar el script SQL
        script_path = r'C:\Users\Alejandro\Downloads\tienda_ddl_inserts.txt'
        with open(script_path, 'r', encoding='utf-8') as file:
            sql_script = file.read()
            
        # Ejecutar el script
        cursor.execute(sql_script)
        print("Script SQL ejecutado correctamente")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        print("Conexión cerrada")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise

if __name__ == '__main__':
    init_database() 