from datetime import datetime
from src.errores.categoria_invalida import CategoriaInvalidaError
from src.errores.fecha_invalida import FechaInvalidaError
from src.errores.venta_producto_no_registrado import VentaProductoNoRegistradoError
from src.errores.venta_invalida import VentaInvalidaError
from src.errores.venta_sin_empleado import VentaSinEmpleadoError
from src.errores.total_invalido import TotalInvalidoError
from src.errores.descuento_invalido import DescuentoInvalidoError
from src.errores.stock_insuficiente import StockInsuficienteError
from typing import List, Tuple, Dict
from src.modelos.inventario import Inventario

CATEGORIAS_VALIDAS = ["electronica", "escolar"]

class Venta:
    """
    Clase que representa una venta en el sistema.
    
    Esta clase maneja la lógica de negocio relacionada con las ventas,
    incluyendo el cálculo de totales y validaciones de productos.

    Attributes:
        id (int): Identificador único de la venta
        fecha (datetime): Fecha y hora de la venta
        productos_vendidos (list): Lista de tuplas (producto, cantidad) vendidos
        id_usuario (int): ID del usuario que realizó la venta
    """

    def __init__(self, id, fecha, productos_vendidos, id_usuario, inventario):
        """
        Inicializa una nueva venta.

        Args:
            id (int): Identificador único de la venta
            fecha (datetime o str): Fecha y hora de la venta (puede ser datetime o string)
            productos_vendidos (list): Lista de tuplas (producto, cantidad) vendidos
            id_usuario (int): ID del usuario que realizó la venta
            inventario (Inventario): Instancia del inventario
        """
        self.id = id
        # Convertir fecha a datetime si es string
        if isinstance(fecha, str):
            try:
                # Intentar formato ISO
                self.fecha = datetime.fromisoformat(fecha)
            except ValueError:
                # Intentar formato DD/MM/AAAA
                try:
                    day, month, year = map(int, fecha.split('/'))
                    if year < 100:
                        year += 2000
                    self.fecha = datetime(year, month, day)
                except Exception:
                    raise ValueError(f"Formato de fecha inválido: {fecha}")
        else:
            self.fecha = fecha
        self.productos_vendidos = productos_vendidos
        self.id_usuario = id_usuario
        self.inventario = inventario
        self.total = self.calcular_total()

        if not id_usuario:
            raise VentaSinEmpleadoError("No se puede crear una venta sin un empleado asignado.")

        # Orden de validaciones:
        # 1. Validar productos registrados
        # 2. Validar categoría
        # 3. Validar cantidades
        # 4. Validar fecha
        # 5. Validar stock
        # 6. Validar venta general
        self._validar_productos_registrados(inventario)
        self._validar_categoria()
        self._validar_cantidades()
        self._validar_fecha(self.fecha)
        self._validar_stock_suficiente(inventario)
        self._validar_venta()

    def validar(self):
        """
        Valida que la venta cumpla con todas las reglas de negocio.
        
        Raises:
            ValueError: Si alguna validación falla
        """
        if not self.productos_vendidos:
            raise ValueError("La venta debe tener al menos un producto")
        for producto, cantidad in self.productos_vendidos:
            if cantidad <= 0:
                raise ValueError(f"La cantidad del producto {producto['nombre']} debe ser mayor a 0")
            if cantidad > producto['cantidad']:
                raise ValueError(f"No hay suficiente stock del producto {producto['nombre']}")

    def calcular_total(self):
        """
        Calcula el total de la venta.
        
        Returns:
            float: Total de la venta
        """
        return sum(producto['precio'] * cantidad for producto, cantidad in self.productos_vendidos)

    def to_dict(self):
        """
        Convierte la venta a un diccionario con los campos necesarios para la base de datos.

        Returns:
            dict: Diccionario con los datos de la venta
        """
        return {
            'fecha': self.fecha,
            'id_usuario': self.id_usuario,
            'total': self.calcular_total()
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crea una venta a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos de la venta
            
        Returns:
            Venta: Nueva instancia de Venta
        """
        productos_vendidos = [
            (Producto.from_dict(item['producto']), item['cantidad'])
            for item in data['productos_vendidos']
        ]
        return cls(
            id=data['id'],
            fecha=data['fecha'],
            productos_vendidos=productos_vendidos,
            id_usuario=data['id_usuario']
        )

    def aplicar_descuento(self, descuento: int):
        """
        Aplica un descuento al total de la venta.

        Args:
            descuento (int): Porcentaje de descuento (0 a 100).

        Raises:
            DescuentoInvalidoError: Si el descuento no está en el rango permitido.
        """
        if descuento < 0 or descuento > 100:
            raise DescuentoInvalidoError("El descuento debe estar entre 0 y 100")
        self.total = max(0, int(self.total * (100 - descuento) / 100))

    def _validar_productos_registrados(self, inventario: Inventario):
        """
        Verifica que todos los productos vendidos estén registrados en el inventario.

        Args:
            inventario (Inventario): Inventario contra el que se valida.

        Raises:
            VentaProductoNoRegistradoError: Si un producto no se encuentra.
        """
        productos_db = inventario.db.get_all_products()
        for producto, _ in self.productos_vendidos:
            if not any(p['nombre'] == producto['nombre'] for p in productos_db):
                raise VentaProductoNoRegistradoError(
                    f"El producto {producto['nombre']} no está registrado en el inventario")

    def _validar_stock_suficiente(self, inventario: Inventario):
        """
        Verifica que haya suficiente stock para todos los productos vendidos.

        Args:
            inventario (Inventario): Inventario contra el que se valida.

        Returns:
            bool: True si hay suficiente stock, False en caso contrario.
        """
        productos_db = inventario.db.get_all_products()
        for producto, cantidad in self.productos_vendidos:
            producto_db = next(p for p in productos_db if p['nombre'] == producto['nombre'])
            if producto_db['cantidad'] < cantidad:
                return False
        return True

    def _validar_fecha(self, fecha):
        """
        Valida y normaliza la fecha ingresada.

        Args:
            fecha (str o datetime): Fecha a validar

        Returns:
            datetime: Fecha validada

        Raises:
            FechaInvalidaError: Si el formato o la fecha son inválidos
        """
        try:
            if isinstance(fecha, str):
                day, month, year = map(int, fecha.split('/'))
                if year < 100:
                    year += 2000
                fecha = datetime(year, month, day)
            
            if fecha > datetime.now():
                raise FechaInvalidaError(f"La fecha {fecha} no puede ser futura")
            
            return fecha
        except (ValueError, AttributeError):
            raise FechaInvalidaError(f"La fecha {fecha} es inválida")

    def _validar_cantidades(self):
        """
        Verifica que las cantidades vendidas sean válidas (> 0).

        Raises:
            VentaInvalidaError: Si alguna cantidad es menor o igual a 0.
        """
        for _, cantidad in self.productos_vendidos:
            if cantidad <= 0:
                raise VentaInvalidaError("La cantidad debe ser mayor a cero")

    def _validar_categoria(self):
        """
        Verifica que los productos pertenezcan a una categoría válida.

        Raises:
            CategoriaInvalidaError: Si alguna categoría es inválida.
        """
        for producto, _ in self.productos_vendidos:
            if producto['categoria'].lower() not in [c.lower() for c in CATEGORIAS_VALIDAS]:
                raise CategoriaInvalidaError(f"La categoría '{producto['categoria']}' no es válida")

    def _validar_venta(self):
        """
        Realiza validaciones generales sobre la venta.

        Raises:
            VentaInvalidaError: Si la venta no tiene productos.
            VentaSinEmpleadoError: Si no hay empleado asignado.
            TotalInvalidoError: Si el total calculado es negativo.
        """
        if not self.productos_vendidos:
            raise VentaInvalidaError("La venta debe incluir al menos un producto")
        if self.id_usuario is None:
            raise VentaSinEmpleadoError("La venta debe estar asociada a un usuario")

        if self.total < 0:
            raise TotalInvalidoError("El total de la venta no puede ser negativo")
