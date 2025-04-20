from src.errores.producto_invalido import ProductoInvalidoError
from src.errores.stock_invalido import StockInvalidoError
from src.errores.precio_invalido import PrecioInvalidoError
from src.errores.categoria_invalida import CategoriaInvalidaError


class Producto:
    """
    Representa un producto dentro del inventario.

    Attributes:
        STOCK_MAXIMO (int): Límite superior de unidades permitidas por producto.
        id (int): Identificador único del producto.
        nombre (str): Nombre del producto.
        precio (float): Precio unitario del producto.
        cantidad (int): Stock actual del producto.
        categoria (str): Categoría a la que pertenece el producto.
        stock_minimo (int): Cantidad mínima permitida antes de considerar reposición.
    """
    
    STOCK_MAXIMO = 1000

    def __init__(self, id: int, nombre: str, precio: float, cantidad: int, categoria: str, stock_minimo: int):
        """
        Inicializa una nueva instancia de Producto con validaciones.

        Args:
            id (int): Identificador del producto.
            nombre (str): Nombre del producto.
            precio (float): Precio del producto (debe ser mayor a 0).
            cantidad (int): Stock actual (no puede ser negativo ni exceder STOCK_MAXIMO).
            categoria (str): Categoría del producto (no puede ser numérica ni vacía).
            stock_minimo (int): Cantidad mínima antes de que se considere bajo stock.

        Raises:
            ProductoInvalidoError: Si el nombre es inválido, la cantidad es negativa o el stock mínimo es inválido.
            CategoriaInvalidaError: Si la categoría es vacía o numérica.
            PrecioInvalidoError: Si el precio es menor o igual a cero.
            StockInvalidoError: Si la cantidad excede el STOCK_MAXIMO.
        """
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
        """
        Actualiza el stock del producto sumando la cantidad indicada.

        Args:
            cantidad (int): Cantidad a agregar al stock actual.

        Raises:
            StockInvalidoError: Si la cantidad es negativa o excede el STOCK_MAXIMO.
        """
        if cantidad < 0:
            raise StockInvalidoError("No se puede reducir el stock a un valor negativo.")
        nuevo_stock = self.cantidad + cantidad
        if nuevo_stock > self.STOCK_MAXIMO:
            raise StockInvalidoError(f"El stock no puede exceder el límite de {self.STOCK_MAXIMO}.")
        self.cantidad = nuevo_stock

    def to_dict(self):
        """
        Convierte el objeto Producto a un diccionario serializable.

        Returns:
            dict: Representación del producto en formato diccionario.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "categoria": self.categoria,
            "stock_minimo": self.stock_minimo
        }
