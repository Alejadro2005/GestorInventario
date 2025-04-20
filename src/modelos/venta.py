from datetime import datetime
from src.errores.categoria_invalida import CategoriaInvalidaError
from src.errores.fecha_invalida import FechaInvalidaError
from src.errores.venta_producto_no_registrado import VentaProductoNoRegistradoError
from src.errores.venta_invalida import VentaInvalidaError
from src.errores.venta_sin_empleado import VentaSinEmpleadoError
from src.errores.total_invalido import TotalInvalidoError
from src.errores.descuento_invalido import DescuentoInvalidoError

CATEGORIAS_VALIDAS = ["electronica", "escolar"]

class Venta:
    """
    Representa una venta realizada en el sistema, incluyendo validaciones de productos, fechas y totales.

    Attributes:
        id (int): Identificador único de la venta.
        fecha (str): Fecha de la venta en formato "DD/MM/AAAA".
        productos_vendidos (list): Lista de tuplas (producto, cantidad).
        id_empleado (int): ID del empleado que realizó la venta.
        total (float): Total calculado de la venta.
    """

    def __init__(self, id: int, fecha: str, productos_vendidos: list, id_empleado: int, inventario):
        """
        Inicializa una instancia de Venta con validaciones.

        Args:
            id (int): Identificador único de la venta.
            fecha (str): Fecha en formato "DD/MM/AAAA".
            productos_vendidos (list): Lista de tuplas (Producto, cantidad).
            id_empleado (int): ID del empleado responsable de la venta.
            inventario (Inventario): Objeto de inventario para validar productos.

        Raises:
            FechaInvalidaError: Si la fecha tiene formato incorrecto o es inválida.
            VentaProductoNoRegistradoError: Si un producto no está en el inventario.
            VentaInvalidaError: Si la cantidad es <= 0 o no hay productos.
            VentaSinEmpleadoError: Si no se asigna un empleado a la venta.
            TotalInvalidoError: Si el total calculado es negativo.
            CategoriaInvalidaError: Si algún producto tiene una categoría no válida.
        """
        self.id = id
        self.fecha = self._validar_fecha(fecha)
        self.productos_vendidos = productos_vendidos
        self._validar_productos_registrados(inventario)
        self._validar_cantidades()
        self._validar_categoria()
        self.id_empleado = id_empleado
        self.total = self.calcular_total()
        self._validar_venta()

    def to_dict(self) -> dict:
        """
        Convierte la venta a un diccionario serializable.

        Returns:
            dict: Representación de la venta en formato dict.
        """
        return {
            "id": self.id,
            "fecha": self.fecha,
            "productos_vendidos": [(p.id, cantidad) for p, cantidad in self.productos_vendidos],
            "id_empleado": self.id_empleado,
            "total": self.total
        }

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

    def calcular_total(self) -> float:
        """
        Calcula el total de la venta en base a productos y cantidades.

        Returns:
            float: Total calculado de la venta.
        """
        return sum(producto.precio * cantidad for producto, cantidad in self.productos_vendidos)

    def _validar_fecha(self, fecha_str: str) -> str:
        """
        Valida y normaliza la fecha ingresada.

        Args:
            fecha_str (str): Fecha en formato "DD/MM/AAAA".

        Returns:
            str: Fecha validada.

        Raises:
            FechaInvalidaError: Si el formato o la fecha son inválidos.
        """
        try:
            day, month, year = map(int, fecha_str.split('/'))
            if year < 100:
                year += 2000
            datetime(year, month, day)
            return fecha_str
        except ValueError:
            raise FechaInvalidaError(f"La fecha {fecha_str} es inválida")

    def _validar_productos_registrados(self, inventario):
        """
        Verifica que todos los productos vendidos estén registrados en el inventario.

        Args:
            inventario (Inventario): Inventario contra el que se valida.

        Raises:
            VentaProductoNoRegistradoError: Si un producto no se encuentra.
        """
        for producto, _ in self.productos_vendidos:
            if not any(p.id == producto.id for p in inventario.productos):
                raise VentaProductoNoRegistradoError(
                    f"El producto {producto.nombre} no está registrado en el inventario")

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
            if producto.categoria.lower() not in [c.lower() for c in CATEGORIAS_VALIDAS]:
                raise CategoriaInvalidaError(f"La categoría '{producto.categoria}' no es válida")

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
        if self.id_empleado is None:
            raise VentaSinEmpleadoError("La venta debe estar asociada a un empleado")

        if self.total < 0:
            raise TotalInvalidoError("El total de la venta no puede ser negativo")
