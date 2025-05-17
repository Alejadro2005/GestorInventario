from src.errores.producto_invalido import ProductoInvalidoError
from src.errores.stock_invalido import StockInvalidoError
from src.errores.precio_invalido import PrecioInvalidoError
from src.errores.categoria_invalida import CategoriaInvalidaError


class Producto:
    """
    Clase que representa un producto en el inventario.
    
    Esta clase maneja la lógica de negocio relacionada con los productos,
    incluyendo validaciones de stock, precios y categorías.

    Attributes:
        STOCK_MAXIMO (int): Cantidad máxima permitida de stock
        id (int): Identificador único del producto
        nombre (str): Nombre del producto
        precio (float): Precio unitario del producto
        cantidad (int): Cantidad en inventario
        categoria (str): Categoría del producto
        stock_minimo (int): Nivel mínimo de stock para alertas
    """
    
    STOCK_MAXIMO = 1000

    def __init__(self, id, nombre, precio, cantidad, categoria, stock_minimo):
        """
        Inicializa un nuevo producto.

        Args:
            id (int): Identificador único del producto
            nombre (str): Nombre del producto
            precio (float): Precio unitario del producto
            cantidad (int): Cantidad inicial en inventario
            categoria (str): Categoría del producto
            stock_minimo (int): Nivel mínimo de stock para alertas
        """
        # Validar nombre
        if not nombre or len(nombre.strip()) == 0:
            raise ProductoInvalidoError("El nombre del producto no puede estar vacío")
        if len(nombre) < 3:
            raise ProductoInvalidoError("El nombre del producto debe tener al menos 3 caracteres")
        # Validar precio
        if precio <= 0:
            raise PrecioInvalidoError("El precio debe ser mayor que cero")
        # Validar cantidad y stock mínimo
        if cantidad < 0:
            raise StockInvalidoError("La cantidad no puede ser negativa")
        if stock_minimo < 0:
            raise StockInvalidoError("El stock mínimo no puede ser negativo")
        if cantidad > self.STOCK_MAXIMO:
            raise StockInvalidoError(f"La cantidad no puede ser mayor a {self.STOCK_MAXIMO}")
        if stock_minimo > self.STOCK_MAXIMO:
            raise StockInvalidoError(f"El stock mínimo no puede ser mayor a {self.STOCK_MAXIMO}")
        # Validar categoría
        if not categoria or len(categoria.strip()) == 0:
            raise CategoriaInvalidaError("La categoría no puede estar vacía")
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.categoria = categoria
        self.stock_minimo = stock_minimo

    def validar(self):
        """
        Valida que el producto cumpla con todas las reglas de negocio.
        
        Raises:
            ValueError: Si alguna validación falla
        """
        if not self.nombre or len(self.nombre) < 3:
            raise ValueError("El nombre del producto debe tener al menos 3 caracteres")
        if self.precio <= 0:
            raise ValueError("El precio debe ser mayor que 0")
        if self.cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        if self.cantidad > self.STOCK_MAXIMO:
            raise ValueError(f"La cantidad no puede ser mayor a {self.STOCK_MAXIMO}")
        if not self.categoria:
            raise ValueError("La categoría es requerida")
        if self.stock_minimo < 0:
            raise ValueError("El stock mínimo no puede ser negativo")
        if self.stock_minimo > self.STOCK_MAXIMO:
            raise ValueError(f"El stock mínimo no puede ser mayor a {self.STOCK_MAXIMO}")

    def actualizar_stock(self, cantidad):
        """
        Actualiza la cantidad en inventario del producto.

        Args:
            cantidad (int): Nueva cantidad en inventario

        Raises:
            ValueError: Si la cantidad no es válida
        """
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        if cantidad > self.STOCK_MAXIMO:
            raise ValueError(f"La cantidad no puede ser mayor a {self.STOCK_MAXIMO}")
        self.cantidad = cantidad

    def to_dict(self):
        """
        Convierte el producto a un diccionario.

        Returns:
            dict: Diccionario con los datos del producto
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'cantidad': self.cantidad,
            'categoria': self.categoria,
            'stock_minimo': self.stock_minimo
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crea un producto a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos del producto
            
        Returns:
            Producto: Nueva instancia de Producto
        """
        return cls(
            id=data['id'],
            nombre=data['nombre'],
            precio=data['precio'],
            cantidad=data['cantidad'],
            categoria=data['categoria'],
            stock_minimo=data['stock_minimo']
        )
