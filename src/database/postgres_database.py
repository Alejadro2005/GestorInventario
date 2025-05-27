import psycopg2
from psycopg2 import Error
from database.database_interface import DatabaseInterface
from errores.database_error import DatabaseError
import os
from dotenv import load_dotenv
import datetime
from psycopg2.extras import RealDictCursor

class PostgresDatabase(DatabaseInterface):
    """
    Implementación de la interfaz de base de datos para PostgreSQL.
    
    Esta clase maneja todas las operaciones de base de datos usando PostgreSQL,
    incluyendo la creación de tablas, conexión, y operaciones CRUD.
    
    Attributes:
        config (dict): Configuración de la base de datos (host, port, dbname, user, password)
        connection: Conexión activa a la base de datos PostgreSQL
    """
    
    def __init__(self, config):
        """
        Inicializa la conexión a la base de datos PostgreSQL.
        
        Args:
            config (dict): Diccionario con la configuración de la base de datos
        """
        self.config = config
        self.connection = None
        self.cursor = None
        load_dotenv()
        
    def connect(self):
        """
        Establece la conexión con la base de datos PostgreSQL.
        
        Raises:
            DatabaseError: Si hay un error al conectar con la base de datos
        """
        try:
            self.connection = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                database=os.getenv('DB_NAME', 'gestor_inventario'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'postgres'),
                port=os.getenv('DB_PORT', '5432')
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        except Error as e:
            raise DatabaseError(f"Error al conectar a PostgreSQL: {str(e)}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None

    def create_tables(self):
        """
        Crea las tablas necesarias en la base de datos si no existen.
        
        Crea las siguientes tablas:
        - usuarios: Almacena información de usuarios del sistema
        - productos: Almacena el catálogo de productos
        - ventas: Registra las ventas realizadas
        - detalle_ventas: Almacena los detalles de cada venta
        
        Raises:
            DatabaseError: Si hay un error al crear las tablas
        """
        try:
            cursor = self.connection.cursor()
            
            # Crear tabla usuarios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    rol VARCHAR(50) NOT NULL,
                    password VARCHAR(100) NOT NULL,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Crear tabla productos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS productos (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    precio DECIMAL(10,2) NOT NULL,
                    cantidad INTEGER NOT NULL,
                    categoria VARCHAR(50) NOT NULL,
                    stock_minimo INTEGER NOT NULL,
                    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Crear tabla ventas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id SERIAL PRIMARY KEY,
                    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    id_usuario INTEGER REFERENCES usuarios(id),
                    total DECIMAL(10,2) NOT NULL
                )
            """)
            
            # Crear tabla detalle_ventas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detalle_ventas (
                    venta_id INTEGER REFERENCES ventas(id),
                    producto_id INTEGER REFERENCES productos(id),
                    cantidad INTEGER NOT NULL,
                    precio DECIMAL(10,2) NOT NULL,
                    PRIMARY KEY (venta_id, producto_id)
                )
            """)
            
            self.connection.commit()
            
            # Actualizar las secuencias después de crear las tablas
            self.actualizar_secuencias()
            
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al crear tablas: {e}")

    def actualizar_secuencias(self):
        """
        Actualiza las secuencias de autoincremento para que coincidan con el máximo ID actual.
        Esto evita conflictos de clave duplicada al insertar nuevos registros.
        """
        try:
            cursor = self.connection.cursor()
            
            # Actualizar secuencia de usuarios
            cursor.execute("""
                SELECT setval('usuarios_id_seq', COALESCE((SELECT MAX(id) FROM usuarios), 1))
            """)
            
            # Actualizar secuencia de productos
            cursor.execute("""
                SELECT setval('productos_id_seq', COALESCE((SELECT MAX(id) FROM productos), 1))
            """)
            
            # Actualizar secuencia de ventas
            cursor.execute("""
                SELECT setval('ventas_id_seq', COALESCE((SELECT MAX(id) FROM ventas), 1))
            """)
            
            self.connection.commit()
            cursor.close()
            
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al actualizar secuencias: {e}")

    def execute_query(self, query, params=None):
        """
        Ejecuta una consulta SQL en la base de datos.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple, optional): Parámetros para la consulta
            
        Returns:
            cursor: Cursor con el resultado de la consulta
            
        Raises:
            DatabaseError: Si hay un error al ejecutar la consulta
        """
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except Error as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al ejecutar query: {str(e)}")

    def fetch_one(self, query, params=None):
        """
        Ejecuta una consulta y retorna un solo resultado.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple, optional): Parámetros para la consulta
            
        Returns:
            tuple: Primera fila del resultado o None si no hay resultados
        """
        cursor = self.execute_query(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all(self, query, params=None):
        """
        Ejecuta una consulta y retorna todos los resultados.
        
        Args:
            query (str): Consulta SQL a ejecutar
            params (tuple, optional): Parámetros para la consulta
            
        Returns:
            list: Lista de tuplas con todos los resultados
        """
        cursor = self.execute_query(query, params)
        result = cursor.fetchall()
        cursor.close()
        return result

    def insert(self, table, data):
        """
        Inserta un nuevo registro en la tabla especificada.
        
        Args:
            table (str): Nombre de la tabla
            data (dict): Diccionario con los datos a insertar
            
        Returns:
            int: ID del registro insertado o None si falla
        """
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({values}) RETURNING id"
        cursor = self.execute_query(query, list(data.values()))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def update(self, table, data, condition):
        """
        Actualiza registros en la tabla especificada.
        
        Args:
            table (str): Nombre de la tabla
            data (dict): Diccionario con los datos a actualizar
            condition (dict): Diccionario con las condiciones de actualización
        """
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = %s" for k in condition.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = list(data.values()) + list(condition.values())
        cursor = self.execute_query(query, params)
        cursor.close()

    def delete(self, table, condition):
        """
        Elimina registros de la tabla especificada.
        
        Args:
            table (str): Nombre de la tabla
            condition (dict): Diccionario con las condiciones de eliminación
        """
        where_clause = ' AND '.join([f"{k} = %s" for k in condition.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        cursor = self.execute_query(query, list(condition.values()))
        cursor.close()

    def drop_tables(self):
        """
        Elimina todas las tablas de la base de datos.
        
        Raises:
            DatabaseError: Si hay un error al eliminar las tablas
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("DROP TABLE IF EXISTS detalle_ventas, ventas, productos, usuarios CASCADE;")
            self.connection.commit()
            cursor.close()
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al eliminar tablas: {e}")

    # USUARIOS
    def insert_user(self, user_data):
        try:
            # Eliminar el campo 'id' si existe
            user_data = user_data.copy()
            user_data.pop('id', None)
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO usuarios (nombre, rol, password) VALUES (%s, %s, %s) RETURNING id",
                (user_data['nombre'], user_data['rol'], user_data['password'])
            )
            user_id = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            return user_id
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al insertar usuario: {e}")

    def create_user(self, user_data):
        # Eliminar el campo 'id' si existe antes de llamar a insert_user
        user_data = user_data.copy()
        user_data.pop('id', None)
        return self.insert_user(user_data)

    def get_user(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, nombre, rol, password, fecha_creacion FROM usuarios WHERE id = %s", (user_id,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return {
                    'id': row[0],
                    'nombre': row[1],
                    'rol': row[2],
                    'password': row[3],
                    'fecha_creacion': row[4]
                }
            return None
        except Exception as e:
            raise DatabaseError(f"Error al obtener usuario: {e}")

    def update_user(self, user_id, user_data):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE usuarios SET nombre=%s, rol=%s, password=%s WHERE id=%s",
                (user_data['nombre'], user_data['rol'], user_data['password'], user_id)
            )
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al actualizar usuario: {e}")

    def delete_user(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM usuarios WHERE id=%s", (user_id,))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al eliminar usuario: {e}")

    # PRODUCTOS
    def insert_product(self, product_data):
        print("DEBUG insert_product:", product_data)
        try:
            # Eliminar el campo 'id' si existe
            product_data = product_data.copy()
            product_data.pop('id', None)
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO productos (nombre, precio, cantidad, categoria, stock_minimo) VALUES (%s, %s, %s, %s, %s) RETURNING id",
                (product_data['nombre'], product_data['precio'], product_data['cantidad'], product_data['categoria'], product_data['stock_minimo'])
            )
            product_id = cursor.fetchone()[0]
            self.connection.commit()
            cursor.close()
            return product_id
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al insertar producto: {e}")

    def get_product(self, product_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, nombre, precio, cantidad, categoria, stock_minimo, fecha_creacion FROM productos WHERE id = %s", (product_id,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return {
                    'id': row[0],
                    'nombre': row[1],
                    'precio': float(row[2]),
                    'cantidad': row[3],
                    'categoria': row[4],
                    'stock_minimo': row[5],
                    'fecha_creacion': row[6]
                }
            return None
        except Exception as e:
            raise DatabaseError(f"Error al obtener producto: {e}")

    def update_product(self, product_id, product_data):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "UPDATE productos SET nombre=%s, precio=%s, cantidad=%s, categoria=%s, stock_minimo=%s WHERE id=%s",
                (product_data['nombre'], product_data['precio'], product_data['cantidad'], product_data['categoria'], product_data['stock_minimo'], product_id)
            )
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al actualizar producto: {e}")

    def delete_product(self, product_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM productos WHERE id=%s", (product_id,))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al eliminar producto: {e}")

    def update_stock(self, product_id, quantity):
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE productos SET cantidad=%s WHERE id=%s", (quantity, product_id))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al actualizar stock: {e}")

    # VENTAS
    def insert_sale(self, sale_data):
        """
        Inserta una nueva venta en la base de datos.
        """
        try:
            # Si no se recibe 'fecha', usar la fecha y hora actual
            if 'fecha' not in sale_data:
                sale_data['fecha'] = datetime.datetime.now()
            # Si el ID está en los datos, usarlo directamente
            if 'id' in sale_data:
                id_venta = sale_data.pop('id')
                query = """
                    INSERT INTO ventas (id, fecha, id_usuario, total)
                    VALUES (%s, %s, %s, %s)
                """
                params = (id_venta, sale_data['fecha'], sale_data['id_usuario'], sale_data['total'])
                cursor = self.execute_query(query, params)
                cursor.close()
                return id_venta
            else:
                query = """
                    INSERT INTO ventas (fecha, id_usuario, total)
                    VALUES (%s, %s, %s)
                    RETURNING id
                """
                params = (sale_data['fecha'], sale_data['id_usuario'], sale_data['total'])
                cursor = self.execute_query(query, params)
                result = cursor.fetchone()
                cursor.close()
                return result[0] if result else None
        except Error as e:
            raise DatabaseError(f"Error al insertar venta: {str(e)}")

    def insert_sale_detail(self, detail_data):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio) VALUES (%s, %s, %s, %s)",
                (detail_data['venta_id'], detail_data['producto_id'], detail_data['cantidad'], detail_data['precio'])
            )
            self.connection.commit()
            cursor.close()
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al insertar detalle de venta: {e}")

    def get_sale(self, sale_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, fecha, id_usuario, total FROM ventas WHERE id = %s", (sale_id,))
            row = cursor.fetchone()
            cursor.close()
            if row:
                return {
                    'id': row[0],
                    'fecha': row[1],
                    'id_usuario': row[2],
                    'total': float(row[3])
                }
            return None
        except Exception as e:
            raise DatabaseError(f"Error al obtener venta: {e}")

    def get_sale_details(self, sale_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT venta_id, producto_id, cantidad, precio FROM detalle_ventas WHERE venta_id = %s", (sale_id,))
            rows = cursor.fetchall()
            detalles = []
            for row in rows:
                detalles.append({
                    'venta_id': row[0],
                    'producto_id': row[1],
                    'cantidad': row[2],
                    'precio': float(row[3])
                })
            cursor.close()
            return detalles
        except Exception as e:
            raise DatabaseError(f"Error al obtener detalles de venta: {e}")

    def get_all_sales(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, fecha, id_usuario, total FROM ventas")
            rows = cursor.fetchall()
            ventas = []
            for row in rows:
                ventas.append({
                    'id': row[0],
                    'fecha': row[1],
                    'id_usuario': row[2],
                    'total': float(row[3])
                })
            cursor.close()
            return ventas
        except Exception as e:
            raise DatabaseError(f"Error al obtener ventas: {e}")

    def get_all_sale_details(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT venta_id, producto_id, cantidad, precio FROM detalle_ventas")
            rows = cursor.fetchall()
            detalles = []
            for row in rows:
                detalles.append({
                    'venta_id': row[0],
                    'producto_id': row[1],
                    'cantidad': row[2],
                    'precio': float(row[3])
                })
            cursor.close()
            return detalles
        except Exception as e:
            raise DatabaseError(f"Error al obtener detalles de ventas: {e}")

    def get_sales_by_user(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, fecha, id_usuario, total FROM ventas WHERE id_usuario = %s", (user_id,))
            rows = cursor.fetchall()
            ventas = []
            for row in rows:
                ventas.append({
                    'id': row[0],
                    'fecha': row[1],
                    'id_usuario': row[2],
                    'total': float(row[3])
                })
            cursor.close()
            return ventas
        except Exception as e:
            raise DatabaseError(f"Error al obtener ventas por usuario: {e}")

    def get_sale_details_by_user(self, user_id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT dv.venta_id, dv.producto_id, dv.cantidad, dv.precio
                FROM detalle_ventas dv
                JOIN ventas v ON dv.venta_id = v.id
                WHERE v.id_usuario = %s
            """, (user_id,))
            rows = cursor.fetchall()
            detalles = []
            for row in rows:
                detalles.append({
                    'venta_id': row[0],
                    'producto_id': row[1],
                    'cantidad': row[2],
                    'precio': float(row[3])
                })
            cursor.close()
            return detalles
        except Exception as e:
            raise DatabaseError(f"Error al obtener detalles de ventas por usuario: {e}")

    def delete_all_sales(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM detalle_ventas;")
            cursor.execute("DELETE FROM ventas;")
            self.connection.commit()
            cursor.close()
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al eliminar todas las ventas: {e}")

    def get_all_users(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, nombre, rol, password, fecha_creacion FROM usuarios")
            rows = cursor.fetchall()
            usuarios = []
            for row in rows:
                usuarios.append({
                    'id': row[0],
                    'nombre': row[1],
                    'rol': row[2],
                    'password': row[3],
                    'fecha_creacion': row[4]
                })
            cursor.close()
            return usuarios
        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            return []

    def get_all_products(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id, nombre, precio, cantidad, categoria, stock_minimo, fecha_creacion FROM productos")
            rows = cursor.fetchall()
            productos = []
            for row in rows:
                productos.append({
                    'id': row[0],
                    'nombre': row[1],
                    'precio': float(row[2]),
                    'cantidad': row[3],
                    'categoria': row[4],
                    'stock_minimo': row[5],
                    'fecha_creacion': row[6]
                })
            cursor.close()
            return productos
        except Exception as e:
            print(f"Error al obtener productos: {e}")
            return []

    def create_sale(self, sale_data):
        return self.insert_sale(sale_data)

    def create_product(self, product_data):
        # Eliminar el campo 'id' si existe antes de llamar a insert_product
        product_data = product_data.copy()
        product_data.pop('id', None)
        return self.insert_product(product_data)

    def get_next_sale_id(self):
        """
        Obtiene el siguiente ID disponible para una nueva venta.
        
        Returns:
            int: El siguiente ID disponible para una venta
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT nextval('ventas_id_seq')")
            next_id = cursor.fetchone()[0]
            cursor.close()
            return next_id
        except Error as e:
            raise DatabaseError(f"Error al obtener siguiente ID de venta: {str(e)}")

    def delete_sale(self, sale_id):
        """
        Elimina una venta y sus detalles de la base de datos.
        """
        try:
            cursor = self.connection.cursor()
            # Eliminar detalles de la venta
            cursor.execute("DELETE FROM detalle_ventas WHERE venta_id = %s", (sale_id,))
            # Eliminar la venta
            cursor.execute("DELETE FROM ventas WHERE id = %s", (sale_id,))
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            self.connection.rollback()
            raise DatabaseError(f"Error al eliminar venta: {e}")

    def tables_exist(self):
        """
        Verifica si las tablas necesarias ya existen en la base de datos.
        :return: True si las tablas existen, False en caso contrario.
        """
        # Aquí puedes usar una consulta SQL para verificar si las tablas existen
        # Por ejemplo, puedes usar una consulta como:
        # SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'nombre_de_la_tabla');
        # Retorna True si las tablas existen, False en caso contrario.
        pass

    def close(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close() 