from src.modelos.inventario import Inventario
from src.modelos.venta import Venta
from src.errores.stock_insuficiente import StockInsuficienteError
from src.errores.venta_producto_no_registrado import VentaProductoNoRegistradoError

class Tienda:
    def __init__(self, inventario: Inventario):
        self.inventario = inventario
        self.db = inventario.db

    def registrar_venta(self, venta: Venta, inventario: Inventario):
        for producto, cantidad in venta.productos_vendidos:
            # Actualizar el stock después de validar
            inventario.reducir_stock(producto['id'], cantidad)

        # Preparar detalles de la venta con el precio actual
        detalles = []
        for producto, cantidad in venta.productos_vendidos:
            detalles.append({
                'id_producto': producto['id'],
                'cantidad': cantidad,
                'precio': producto['precio'],
                'producto_nombre': producto['nombre']
            })

        venta_data = {
            'id': venta.id,
            'fecha': venta.fecha,
            'id_usuario': venta.id_empleado,
            'total': venta.total,
            'detalles': detalles
        }
        self.db.create_sale(venta_data)
        return f"Venta registrada con éxito. Total: {venta.total}"

    def generar_historial(self):
        ventas = self.db.get_all_sales()
        historial = []
        for v in ventas:
            productos = [f"{d['producto_nombre']} (x{d['cantidad']})" for d in v['detalles']]
            historial.append({
                "id": v['id'],
                "fecha": v['fecha'],
                "productos": productos,
                "total": v['total'],
                "empleado": v['id_usuario']
            })
        return historial

    def validar_stock_venta(self, id_producto: int, cantidad: int, inventario: Inventario) -> bool:
        productos_db = inventario.db.get_all_products()
        producto = next((p for p in productos_db if p['id'] == id_producto), None)
        return producto is not None and producto['cantidad'] >= cantidad

    def borrar_historial_ventas(self):
        self.db.delete_all_sales()
        return "Historial de ventas borrado correctamente."
