import os
from src.modulos.persistencia import PersistenciaJSON
from src.modelos.inventario import Inventario
from src.modelos.venta import Venta
from src.errores.stock_insuficiente import StockInsuficienteError
from src.errores.venta_producto_no_registrado import VentaProductoNoRegistradoError

RUTA_VENTAS = "data/ventas.json"


class Tienda:
    def __init__(self, inventario: Inventario):
        """
        Inicializa la tienda con el inventario y carga el historial de ventas.

        Args:
            inventario (Inventario): El inventario asociado a la tienda.

        Returns:
            None
        """
        self.inventario = inventario
        self.historial_ventas = self.cargar_ventas()

    def cargar_ventas(self):
        """
        Carga el historial de ventas desde un archivo JSON utilizando PersistenciaJSON.

        Returns:
            list: Una lista de objetos de venta reconstruidos a partir de los datos cargados.
        """
        datos = PersistenciaJSON.cargar_datos(RUTA_VENTAS)
        return [self._reconstruir_venta(v) for v in datos]

    def _reconstruir_venta(self, datos_venta):
        """
        Reconstruye una venta a partir de los datos cargados desde el archivo.

        Args:
            datos_venta (dict): Un diccionario con los datos de una venta.

        Returns:
            Venta: Un objeto de la clase Venta reconstruido a partir de los datos.
        """
        productos_vendidos = []
        for item in datos_venta.get("productos_vendidos", []):
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
        """
        Guarda el historial de ventas en un archivo JSON utilizando PersistenciaJSON.

        Returns:
            None
        """
        datos = [venta.to_dict() for venta in self.historial_ventas]
        PersistenciaJSON.guardar_datos(RUTA_VENTAS, datos)

    def registrar_venta(self, venta: Venta, inventario: Inventario):
        """
        Registra una nueva venta, validando el stock y reduciendo el inventario.

        Args:
            venta (Venta): La venta a registrar.
            inventario (Inventario): El inventario asociado a la tienda.

        Returns:
            str: Mensaje de éxito con el total de la venta.

        Raises:
            VentaProductoNoRegistradoError: Si algún producto no está registrado en el inventario.
            StockInsuficienteError: Si no hay suficiente stock para alguno de los productos vendidos.
        """
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
        """
        Genera un historial de ventas con formato amigable y nombres reales.

        Returns:
            list: Una lista de diccionarios representando el historial de ventas, con formato amigable.
        """
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
        """
        Valida si hay suficiente stock de un producto para realizar una venta.

        Args:
            id_producto (int): El ID del producto que se quiere validar.
            cantidad (int): La cantidad que se quiere vender.
            inventario (Inventario): El inventario de la tienda.

        Returns:
            bool: `True` si hay suficiente stock, `False` en caso contrario.
        """
        producto = next((p for p in inventario.productos if p.id == id_producto), None)
        return producto is not None and producto.cantidad >= cantidad
