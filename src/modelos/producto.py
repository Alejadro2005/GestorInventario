from src.errores.producto_invalido import ProductoInvalidoError
from src.errores.stock_invalido import StockInvalidoError
from src.errores.precio_invalido import PrecioInvalidoError
from src.errores.categoria_invalida import CategoriaInvalidaError


class Producto:
    STOCK_MAXIMO = 1000

    def __init__(self, id: int, nombre: str, precio: float, cantidad: int, categoria: str, stock_minimo: int):
        if not nombre or any(char in nombre for char in "@!#$%^&*()"):
            raise ProductoInvalidoError(
                "El nombre del producto no puede estar vacío ni contener caracteres especiales.")
        if not categoria or categoria.isnumeric():
            raise CategoriaInvalidaError("La categoría del producto no puede estar vacía ni ser numérica.")
        if precio <= 0:
            raise PrecioInvalidoError("El precio del producto debe ser mayor a cero.")
        if cantidad < 0:
            raise ProductoInvalidoError("La cantidad del producto no puede ser negativa.")
        if cantidad > self.STOCK_MAXIMO:
            raise StockInvalidoError(f"El stock no puede exceder el límite de {self.STOCK_MAXIMO}.")
        if stock_minimo < 0:
            raise ProductoInvalidoError("El stock mínimo no puede ser negativo.")

        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.categoria = categoria
        self.stock_minimo = stock_minimo

    def actualizar_stock(self, cantidad: int):
        """Actualiza la cantidad de stock del producto."""
        if cantidad < 0:
            raise StockInvalidoError("No se puede reducir el stock a un valor negativo.")
        nuevo_stock = self.cantidad + cantidad
        if nuevo_stock > self.STOCK_MAXIMO:
            raise StockInvalidoError(f"El stock no puede exceder el límite de {self.STOCK_MAXIMO}.")
        self.cantidad = nuevo_stock

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "categoria": self.categoria,
            "stock_minimo": self.stock_minimo
        }
