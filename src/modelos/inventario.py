import os
import json
from src.modelos.producto import Producto
from src.errores.producto_invalido import ProductoInvalidoError
from src.errores.producto_no_encontrado import ProductoNoEncontradoError
from src.errores.productos_duplicados import ProductoDuplicadoError
from src.errores.stock_invalido import StockInvalidoError
from src.errores.no_hay_productos import NoHayProductosError
from src.errores.stock_insuficiente import StockInsuficienteError
from src.database.database_interface import DatabaseInterface
import logging
from typing import List

RUTA_INVENTARIO = "data/inventario.json"
logger = logging.getLogger(__name__)


class Inventario:
    """
    Clase que representa el inventario de productos del sistema.
    
    Esta clase maneja la lógica de negocio relacionada con la gestión de productos,
    incluyendo agregar, actualizar, eliminar y consultar productos, así como la gestión de stock.

    Attributes:
        db: Instancia de la base de datos utilizada para persistencia
    """

    def __init__(self, db: DatabaseInterface):
        """
        Inicializa el inventario con una instancia de base de datos.

        Args:
            db: Instancia de la base de datos
        """
        self.db = db

    def cargar_inventario(self):
        """
        Carga el inventario desde un archivo JSON.

        Si el archivo no existe o está vacío, inicializa una lista vacía de productos.
        """
        if not os.path.exists(RUTA_INVENTARIO):
            self.productos = []
            return

        try:
            with open(RUTA_INVENTARIO, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                self.productos = [Producto.from_dict(p) for p in datos]
        except json.JSONDecodeError:
            self.productos = []

    def guardar_inventario(self):
        """
        Guarda los productos actuales en el archivo JSON de inventario.
        """
        os.makedirs(os.path.dirname(RUTA_INVENTARIO), exist_ok=True)
        with open(RUTA_INVENTARIO, "w", encoding="utf-8") as archivo:
            json.dump([p.__dict__ for p in self.productos], archivo, indent=4, ensure_ascii=False)

    def agregar_producto(self, producto: Producto) -> int:
        """
        Agrega un nuevo producto al inventario.
        
        Args:
            producto (Producto): Producto a agregar
        
        Returns:
            int: ID del producto agregado
        """
        return self.db.create_product(producto.to_dict())

    def obtener_producto(self, id_producto: int) -> Producto:
        """
        Obtiene un producto por su ID.

        Args:
            id_producto (int): ID del producto
        
        Returns:
            Producto o None si no existe
        """
        producto = self.db.get_product(id_producto)
        if producto:
            return Producto.from_dict(producto)
        return None

    def modificar_producto(self, id_producto: int, producto: Producto) -> bool:
        """
        Modifica un producto existente.

        Args:
            id_producto (int): ID del producto a modificar.
            producto (Producto): Nuevos datos del producto.

        Returns:
            bool: True si se modificó correctamente, False en caso contrario.

        Raises:
            ProductoNoEncontradoError: Si el producto no está registrado.
        """
        producto_actual = self.obtener_producto(id_producto)
        if not producto_actual:
            raise ProductoNoEncontradoError(f"No se encontró un producto con ID {id_producto}.")
        return self.db.update_product(id_producto, producto.to_dict())

    def eliminar_producto(self, id_producto: int) -> str:
        """
        Elimina un producto del inventario por su ID.

        Args:
            id_producto (int): ID del producto a eliminar

        Returns:
            str: Mensaje de confirmación
        """
        producto = self.obtener_producto(id_producto)
        if not producto:
            raise ProductoNoEncontradoError(f"No se encontró un producto con ID {id_producto}.")
        if self.db.delete_product(id_producto):
            return f"El producto '{producto.nombre}' ha sido eliminado con éxito."
        return "Error al eliminar el producto."

    def filtrar_por_stock_bajo(self) -> List[Producto]:
        """
        Retorna una lista de productos con stock bajo.

        Returns:
            List[Producto]: Lista de productos con stock bajo.

        Raises:
            NoHayProductosError: Si no hay productos en el inventario.
        """
        productos = self.db.get_all_products()
        if not productos:
            raise NoHayProductosError("No hay productos en el inventario.")
        
        productos_stock_bajo = []
        for p in productos:
            producto = Producto.from_dict(p)
            if producto.cantidad <= producto.stock_minimo:
                productos_stock_bajo.append(producto)
        
        return productos_stock_bajo

    def actualizar_stock(self, id_producto: int, cantidad: int) -> str:
        """
        Actualiza el stock de un producto al valor absoluto indicado.

        Args:
            id_producto (int): ID del producto
            cantidad (int): Nuevo valor de stock

        Returns:
            str: Mensaje de confirmación

        Raises:
            StockInvalidoError: Si el stock es negativo
        """
        if cantidad < 0:
            raise StockInvalidoError("No se puede actualizar el stock a un valor negativo")
        self.db.update_stock(id_producto, cantidad)
        return f"Stock actualizado a {cantidad} unidades."

    def reducir_stock(self, id_producto: int, cantidad: int) -> str:
        """
        Reduce el stock de un producto en la cantidad indicada.

        Args:
            id_producto (int): ID del producto
            cantidad (int): Cantidad a reducir

        Returns:
            str: Mensaje de confirmación

        Raises:
            StockInvalidoError: Si el stock resultante es negativo
        """
        producto = self.obtener_producto(id_producto)
        if not producto:
            raise ProductoNoEncontradoError(f"No se encontró un producto con ID {id_producto}")
        nuevo_stock = producto.cantidad - cantidad
        if nuevo_stock < 0:
            raise StockInvalidoError("No hay suficiente stock para realizar la operación")
        self.db.update_stock(id_producto, nuevo_stock)
        return f"Stock reducido a {nuevo_stock} unidades."

    def close(self):
        """Cierra la conexión a la base de datos asociada al inventario."""
        if hasattr(self, 'db') and hasattr(self.db, 'disconnect'):
            self.db.disconnect()

    def actualizar_cache(self):
        """
        Actualiza el caché del inventario con los datos más recientes de la base de datos.
        """
        try:
            productos_db = self.db.get_all_products()
            self.productos = [Producto.from_dict(p) for p in productos_db]
            logger.info("Caché de inventario actualizado correctamente")
        except Exception as e:
            logger.error(f"Error al actualizar caché de inventario: {str(e)}")
            raise

    def listar_productos(self):
        """
        Retorna una lista de todos los productos en el inventario.
        
        Returns:
            list: Lista de instancias de Producto
        """
        productos_data = self.db.get_all_products()
        return [Producto.from_dict(p) for p in productos_data]
