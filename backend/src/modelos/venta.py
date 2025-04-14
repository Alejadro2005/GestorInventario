from datetime import datetime
from src.modelos.inventario import Inventario
from src.errores.fecha_invalida import FechaInvalidaError
from src.errores.venta_invalida import VentaInvalidaError
from src.errores.total_invalido import TotalInvalidoError
from src.errores.venta_sin_empleado import VentaSinEmpleadoError
from src.errores.venta_producto_no_registrado import VentaProductoNoRegistradoError
from src.errores.descuento_invalido import DescuentoInvalidoError
from src.errores.categoria_invalida import CategoriaInvalidaError

CATEGORIAS_VALIDAS = ["electronica", "escolar"]


class Venta:
    def __init__(self, id: int, fecha: str, productos_vendidos: list, id_empleado: int, inventario: Inventario):
        self.id = id
        self.fecha = self._validar_fecha(fecha)
        self.productos_vendidos = productos_vendidos
        self._validar_productos_registrados(inventario)
        self._validar_cantidades()
        self._validar_categoria()
        self.id_empleado = id_empleado
        self.total = self.calcular_total()
        self._validar_venta()

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "productos_vendidos": [
                {"id_producto": p.id, "cantidad": c}  # ✔️ Guardar como diccionario
                for p, c in self.productos_vendidos
            ],
            "id_empleado": self.id_empleado,
            "total": self.total
        }

    def _validar_categoria(self):
        for producto, _ in self.productos_vendidos:
            if producto.categoria.lower() not in [c.lower() for c in CATEGORIAS_VALIDAS]:
                raise CategoriaInvalidaError(f"La categoría '{producto.categoria}' no es válida")

    def _validar_fecha(self, fecha_str: str) -> str:
        try:
            day, month, year = map(int, fecha_str.split('/'))
            if year < 100:
                year += 2000
            datetime(year, month, day)
            return fecha_str
        except ValueError:
            raise FechaInvalidaError(f"La fecha {fecha_str} es inválida")

    def _validar_productos_registrados(self, inventario: Inventario):
        for producto, _ in self.productos_vendidos:
            if not any(p.id == producto.id for p in inventario.productos):
                raise VentaProductoNoRegistradoError(
                    f"El producto {producto.nombre} no está registrado en el inventario")

    def _validar_cantidades(self):
        for _, cantidad in self.productos_vendidos:
            if cantidad <= 0:
                raise VentaInvalidaError("La cantidad debe ser mayor a cero")

    def _validar_venta(self):
        if not self.productos_vendidos:
            raise VentaInvalidaError("La venta debe incluir al menos un producto")
        if self.id_empleado is None:
            raise VentaSinEmpleadoError("La venta debe estar asociada a un empleado")

        # Validación del total después de verificar cantidades
        if self.total < 0:
            raise TotalInvalidoError("El total de la venta no puede ser negativo")

    def calcular_total(self):
        return sum(producto.precio * cantidad for producto, cantidad in self.productos_vendidos)

    def aplicar_descuento(self, descuento: int):
        if descuento < 0 or descuento > 100:
            raise DescuentoInvalidoError("El descuento debe estar entre 0 y 100")
        self.total = max(0, int(self.total * (100 - descuento) / 100))

    def to_dict(self):
        return {
            "id": self.id,
            "fecha": self.fecha,
            "productos_vendidos": [(p.id, cantidad) for p, cantidad in self.productos_vendidos],
            "id_empleado": self.id_empleado,
            "total": self.total
        }
