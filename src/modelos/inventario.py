import os
import json
from src.modelos.producto import Producto
from src.errores.producto_invalido import ProductoInvalidoError
from src.errores.producto_no_encontrado import ProductoNoEncontradoError
from src.errores.productos_duplicados import ProductoDuplicadoError
from src.errores.stock_invalido import StockInvalidoError
from src.errores.no_hay_productos import NoHayProductosError
from src.errores.stock_insuficiente import StockInsuficienteError

RUTA_INVENTARIO = "data/inventario.json"


class Inventario:
    def __init__(self, productos: list[Producto] = None):
        self.productos = productos if productos is not None else []

    def cargar_inventario(self):
        """Carga los productos desde el archivo JSON."""
        if not os.path.exists(RUTA_INVENTARIO):
            return []
        try:
            with open(RUTA_INVENTARIO, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                return [Producto(**p) for p in datos]
        except json.JSONDecodeError:
            return []

    def guardar_inventario(self):
        """Guarda los productos en el archivo JSON."""
        with open(RUTA_INVENTARIO, "w", encoding="utf-8") as archivo:
            json.dump([p.__dict__ for p in self.productos], archivo, indent=4, ensure_ascii=False)

    def agregar_producto(self, producto: Producto):
        """Agrega un producto al inventario, verificando que no esté duplicado."""
        if not producto.nombre:
            raise ProductoInvalidoError("El nombre del producto no puede estar vacío.")
        if any(p.id == producto.id for p in self.productos):
            raise ProductoDuplicadoError(f"El producto con ID {producto.id} ya existe en el inventario.")
        self.productos.append(producto)
        self.guardar_inventario()

    def eliminar_producto(self, id_producto: int) -> str:
        """Elimina un producto del inventario por su ID o lanza un error si no existe."""
        for producto in self.productos:
            if producto.id == id_producto:
                self.productos.remove(producto)
                self.guardar_inventario()
                return f"El producto '{producto.nombre}' ha sido eliminado con éxito."
        raise ProductoNoEncontradoError(f"No se encontró un producto con ID {id_producto}.")

    def filtrar_por_stock_bajo(self) -> list[Producto]:
        """Devuelve una lista de productos con el menor stock en el inventario o lanza un error si no hay productos."""
        if not self.productos:
            raise NoHayProductosError("No hay productos en el inventario para filtrar.")
        min_stock = min(p.cantidad for p in self.productos)
        return [p for p in self.productos if p.cantidad == min_stock]

    def actualizar_stock(self, id_producto: int, cantidad: int) -> str:
        """Actualiza la cantidad de stock de un producto dado su ID o lanza un error si el ID no existe o la cantidad es negativa."""
        if cantidad < 0:
            raise StockInvalidoError("No se puede actualizar el stock con una cantidad negativa.")

        for producto in self.productos:
            if producto.id == id_producto:
                producto.actualizar_stock(cantidad)
                self.guardar_inventario()
                return f"La cantidad de '{producto.nombre}' se ha actualizado a: {producto.cantidad}."

        raise ProductoNoEncontradoError(f"No se encontró un producto con ID {id_producto}.")

    def reducir_stock(self, id_producto: int, cantidad: int):
        """Reduce el stock de un producto si hay suficiente cantidad disponible."""
        if cantidad <= 0:
            raise StockInvalidoError("La cantidad a reducir debe ser mayor a cero.")

        for producto in self.productos:
            if producto.id == id_producto:
                if producto.cantidad >= cantidad:
                    producto.cantidad -= cantidad
                    self.guardar_inventario()
                    return f"Se han descontado {cantidad} unidades de '{producto.nombre}'. Stock actual: {producto.cantidad}."
                else:
                    raise StockInsuficienteError(
                        f"Stock insuficiente para el producto '{producto.nombre}'. Disponible: {producto.cantidad}, requerido: {cantidad}.")

        raise ProductoNoEncontradoError(f"No se encontró un producto con ID {id_producto}.")
