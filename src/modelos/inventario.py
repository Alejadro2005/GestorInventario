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

RUTA_INVENTARIO = "data/inventario.json"


class Inventario:
    """
    Representa el inventario de productos.

    Permite cargar, guardar, agregar, eliminar, actualizar y filtrar productos.
    Utiliza una base de datos para la persistencia de los datos.
    """

    def __init__(self, db: DatabaseInterface):
        """
        Inicializa una instancia de Inventario.

        Args:
            db (DatabaseInterface): Instancia de la interfaz de base de datos.
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
                self.productos = [Producto(**p) for p in datos]
        except json.JSONDecodeError:
            self.productos = []

    def guardar_inventario(self):
        """
        Guarda los productos actuales en el archivo JSON de inventario.
        """
        os.makedirs(os.path.dirname(RUTA_INVENTARIO), exist_ok=True)
        with open(RUTA_INVENTARIO, "w", encoding="utf-8") as archivo:
            json.dump([p.__dict__ for p in self.productos], archivo, indent=4, ensure_ascii=False)

    def agregar_producto(self, producto: Producto):
        """
        Agrega un nuevo producto al inventario si no está duplicado.

        Args:
            producto (Producto): Producto a agregar.

        Raises:
            ProductoInvalidoError: Si el nombre del producto está vacío.
            ProductoDuplicadoError: Si ya existe un producto con el mismo ID.
        """
        if not producto.nombre:
            raise ProductoInvalidoError("El nombre del producto no puede estar vacío.")
        
        try:
            self.db.create_product(producto.__dict__)
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                raise ProductoDuplicadoError(f"El producto con ID {producto.id} ya existe en el inventario.")
            raise e

    def eliminar_producto(self, id_producto: int) -> str:
        """
        Elimina un producto del inventario por su ID.

        Args:
            id_producto (int): ID del producto a eliminar.

        Returns:
            str: Mensaje de éxito.

        Raises:
            ProductoNoEncontradoError: Si el producto con ese ID no existe.
        """
        producto = self.db.get_product(id_producto)
        if not producto:
            raise ProductoNoEncontradoError(f"No se encontró un producto con ID {id_producto}.")
        
        if self.db.delete_product(id_producto):
            return f"El producto '{producto['nombre']}' ha sido eliminado con éxito."
        raise ProductoNoEncontradoError(f"No se encontró un producto con ID {id_producto}.")

    def filtrar_por_stock_bajo(self) -> list[Producto]:
        """
        Filtra y devuelve los productos con el menor stock del inventario.

        Returns:
            list[Producto]: Lista de productos con el stock más bajo.

        Raises:
            NoHayProductosError: Si el inventario está vacío.
        """
        productos = self.db.get_all_products()
        if not productos:
            raise NoHayProductosError("No hay productos en el inventario para filtrar.")
        min_stock = min(p['cantidad'] for p in productos)
        return [Producto(**{k: v for k, v in p.items() if k != 'fecha_creacion'}) for p in productos if p['cantidad'] == min_stock]

    def actualizar_stock(self, id_producto: int, cantidad: int) -> str:
        """
        Actualiza la cantidad de stock de un producto por su ID.

        Args:
            id_producto (int): ID del producto a actualizar.
            cantidad (int): Nueva cantidad de stock.

        Returns:
            str: Mensaje de confirmación.

        Raises:
            StockInvalidoError: Si la cantidad es negativa.
            ProductoNoEncontradoError: Si el producto no existe.
        """
        if cantidad < 0:
            raise StockInvalidoError("No se puede actualizar el stock con una cantidad negativa.")

        producto = self.db.get_product(id_producto)
        if not producto:
            raise ProductoNoEncontradoError(f"No se encontró un producto con ID {id_producto}.")

        producto['cantidad'] = cantidad
        if self.db.update_product(id_producto, producto):
            return f"La cantidad de '{producto['nombre']}' se ha actualizado a: {cantidad}."
        raise ProductoNoEncontradoError(f"No se encontró un producto con ID {id_producto}.")

    def reducir_stock(self, id_producto: int, cantidad: int) -> str:
        """
        Reduce el stock de un producto si hay suficiente cantidad disponible.

        Args:
            id_producto (int): ID del producto a reducir.
            cantidad (int): Cantidad a descontar.

        Returns:
            str: Mensaje de confirmación.

        Raises:
            StockInvalidoError: Si la cantidad es menor o igual a cero.
            StockInsuficienteError: Si no hay suficiente stock disponible.
            ProductoNoEncontradoError: Si el producto no existe.
        """
        if cantidad <= 0:
            raise StockInvalidoError("La cantidad a reducir debe ser mayor a cero.")

        producto = self.db.get_product(id_producto)
        if not producto:
            raise ProductoNoEncontradoError(f"No se encontró un producto con ID {id_producto}.")

        if producto['cantidad'] >= cantidad:
            nueva_cantidad = producto['cantidad'] - cantidad
            producto['cantidad'] = nueva_cantidad
            if self.db.update_product(id_producto, producto):
                return f"Se han descontado {cantidad} unidades de {producto['nombre']}. Stock actual: {nueva_cantidad}."
        else:
            raise StockInsuficienteError(
                f"Stock insuficiente para el producto {producto['nombre']}. Disponible: {producto['cantidad']}, requerido: {cantidad}.")

        raise ProductoNoEncontradoError(f"No se encontró un producto con ID {id_producto}.")

    def close(self):
        """Cierra la conexión a la base de datos asociada al inventario."""
        if hasattr(self, 'db') and hasattr(self.db, 'disconnect'):
            self.db.disconnect()
