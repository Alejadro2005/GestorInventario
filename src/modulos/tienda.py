import os
from src.modulos.persistencia import PersistenciaJSON
from src.modelos.inventario import Inventario
from src.modelos.venta import Venta
from src.errores.stock_insuficiente import StockInsuficienteError
from src.errores.venta_producto_no_registrado import VentaProductoNoRegistradoError

RUTA_VENTAS = "data/ventas.json"


class Tienda:
    def __init__(self, inventario: Inventario):
        self.inventario = inventario
        self.historial_ventas = self.cargar_ventas()

    def cargar_ventas(self):
        """Carga el historial de ventas usando PersistenciaJSON"""
        datos = PersistenciaJSON.cargar_datos(RUTA_VENTAS)
        return [self._reconstruir_venta(v) for v in datos]

    def _reconstruir_venta(self, datos_venta):
        productos_vendidos = []
        for item in datos_venta.get("productos_vendidos", []):
            # Manejar formato antiguo (listas) y nuevo (diccionarios)
            if isinstance(item, list):  # Formato antiguo: [id, cantidad]
                producto_id, cantidad = item[0], item[1]
            else:  # Formato nuevo: {"id_producto": X, "cantidad": Y}
                producto_id = item.get("id_producto")
                cantidad = item.get("cantidad")

            producto = next((p for p in self.inventario.productos if p.id == producto_id), None)
            if producto:
                productos_vendidos.append((producto, cantidad))

        return Venta(
            datos_venta["id"],
            datos_venta["fecha"],
            productos_vendidos,
            datos_venta["id_empleado"],
            self.inventario
        )

    def guardar_ventas(self):
        """Guarda usando PersistenciaJSON y manteniendo formato"""
        datos = [venta.to_dict() for venta in self.historial_ventas]
        PersistenciaJSON.guardar_datos(RUTA_VENTAS, datos)

    def registrar_venta(self, venta: Venta, inventario: Inventario):
        """Versión original con validaciones preservadas"""
        for producto, cantidad in venta.productos_vendidos:
            producto_en_inventario = next((p for p in inventario.productos if p.id == producto.id), None)

            if not producto_en_inventario:
                raise VentaProductoNoRegistradoError(
                    f"El producto {producto.nombre} no está registrado en el inventario")

            if producto_en_inventario.cantidad < cantidad:
                raise StockInsuficienteError(f"Stock insuficiente para el producto {producto.nombre}")

        for producto, cantidad in venta.productos_vendidos:
            inventario.reducir_stock(producto.id, cantidad)

        self.historial_ventas.append(venta)
        self.guardar_ventas()
        return f"Venta registrada con éxito. Total: {venta.total}"

    def generar_historial(self):
        """Muestra nombres reales con formato amigable"""
        return [
            {
                "id": v.id,
                "fecha": v.fecha,
                "productos": [f"{p.nombre} (x{c})" for p, c in v.productos_vendidos],
                "total": v.total,
                "empleado": v.id_empleado
            } for v in self.historial_ventas
        ]

    def validar_stock_venta(self, id_producto: int, cantidad: int, inventario: Inventario) -> bool:
        """Método original sin modificaciones para los tests"""
        producto = next((p for p in inventario.productos if p.id == id_producto), None)
        return producto is not None and producto.cantidad >= cantidad