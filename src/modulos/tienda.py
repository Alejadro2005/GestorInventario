from src.modelos.inventario import Inventario
from src.modelos.venta import Venta
from src.errores.stock_insuficiente import StockInsuficienteError
from src.errores.venta_producto_no_registrado import VentaProductoNoRegistradoError
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class Tienda:
    """
    Clase que representa la lógica de ventas y gestión de historial en la tienda.
    
    Esta clase maneja el registro de ventas, validación de stock, y generación de historial de ventas.
    
    Attributes:
        db: Instancia de la base de datos utilizada para persistencia
        inventario: Instancia del inventario de productos
    """
    
    def __init__(self, db, inventario):
        """
        Inicializa la tienda con la base de datos y el inventario.
        
        Args:
            db: Instancia de la base de datos
            inventario: Instancia del inventario
        """
        self.db = db
        self.inventario = inventario

    def registrar_venta(self, venta, inventario):
        """
        Registra una nueva venta en el sistema.
        Valida existencia y stock de todos los productos antes de descontar stock o registrar la venta.
        Si hay algún error, aborta la operación y muestra un mensaje claro. Solo descuenta stock y registra la venta si todo es válido.
        
        Args:
            venta (Venta): Venta a registrar
            inventario (Inventario): Inventario para actualizar stock
        
        Returns:
            int: ID de la venta registrada
        
        Raises:
            StockInsuficienteError: Si no hay suficiente stock para algún producto
            ProductoNoEncontradoError: Si algún producto no existe
        """
        try:
            # Validar existencia y stock de todos los productos antes de modificar nada
            productos_db = inventario.db.get_all_products()
            for producto, cantidad in venta.productos_vendidos:
                producto_db = next((p for p in productos_db if p['id'] == producto['id']), None)
                if not producto_db:
                    raise VentaProductoNoRegistradoError(f"Producto con ID {producto['id']} no encontrado.")
                if producto_db['cantidad'] < cantidad:
                    raise StockInsuficienteError(f"Stock insuficiente para el producto {producto['nombre']}. Disponible: {producto_db['cantidad']}, requerido: {cantidad}.")

            # Si todo es válido, descontar stock y registrar la venta
            for producto, cantidad in venta.productos_vendidos:
                inventario.reducir_stock(producto['id'], cantidad)

            # Obtener el siguiente ID de venta
            venta_id = self.db.get_next_sale_id()

            # Registrar la venta
            venta_dict = {
                'id': venta_id,
                'fecha': venta.fecha,
                'id_usuario': venta.id_usuario,
                'total': venta.calcular_total()
            }
            self.db.insert_sale(venta_dict)

            # Registrar detalles de la venta
            for producto, cantidad in venta.productos_vendidos:
                detalle = {
                    'venta_id': venta_id,
                    'producto_id': producto['id'],
                    'cantidad': cantidad,
                    'precio': producto['precio']
                }
                self.db.insert_sale_detail(detalle)

            return venta_id

        except Exception as e:
            # Si algo falla, revertir los cambios en el stock
            for producto, cantidad in venta.productos_vendidos:
                try:
                    inventario.actualizar_stock(producto['id'], producto['cantidad'])
                except:
                    pass  # Ignorar errores al revertir
            raise e

    def generar_historial(self):
        """
        Genera un historial de ventas con información detallada.
        
        Returns:
            List[Dict]: Lista de diccionarios con información de cada venta
        """
        try:
            ventas = self.db.get_all_sales()
            if not ventas:
                return []

            historial = []
            productos_db = {p['id']: p['nombre'] for p in self.db.get_all_products()}
            usuarios_db = {u['id']: u['nombre'] for u in self.db.get_all_users()}

            for venta in ventas:
                productos = []
                detalles = self.db.get_sale_details(venta['id'])
                for detalle in detalles:
                    producto_id = detalle['producto_id']
                    nombre = productos_db.get(producto_id, f"ID {producto_id}")
                    cantidad = detalle['cantidad']
                    precio = detalle['precio']
                    productos.append(f"{nombre} (x{cantidad}) - ${precio:,.2f}")

                # Formatear fecha
                fecha = venta['fecha'].strftime('%d/%m/%Y %H:%M') if hasattr(venta['fecha'], 'strftime') else str(venta['fecha'])
                
                historial.append({
                    'id': venta['id'],
                    'fecha': fecha,
                    'productos': productos,
                    'total': venta['total'],
                    'empleado': usuarios_db.get(venta['id_usuario'], f"ID {venta['id_usuario']}")
                })
            return historial
        except Exception as e:
            logger.error(f"Error al generar historial: {str(e)}")
            return []

    def obtener_ventas_usuario(self, id_usuario: int) -> List[Dict]:
        """
        Obtiene las ventas realizadas por un usuario.

        Args:
            id_usuario (int): ID del usuario.

        Returns:
            List[Dict]: Lista de ventas del usuario.
        """
        return self.db.get_sales_by_user(id_usuario)

    def calcular_total_ventas(self) -> float:
        """
        Calcula el total de todas las ventas.

        Returns:
            float: Total de ventas.
        """
        ventas = self.db.get_all_sales()
        return sum(v['total'] for v in ventas)

    def validar_stock_venta(self, id_producto: int, cantidad: int, inventario: Inventario) -> bool:
        """
        Valida si hay suficiente stock para realizar una venta.

        Args:
            id_producto (int): ID del producto a validar
            cantidad (int): Cantidad requerida para la venta
            inventario (Inventario): Instancia del inventario para verificar stock

        Returns:
            bool: True si hay suficiente stock, False en caso contrario
        """
        productos_db = inventario.db.get_all_products()
        producto = next((p for p in productos_db if p['id'] == id_producto), None)
        return producto is not None and producto['cantidad'] >= cantidad

    def borrar_historial_ventas(self):
        """
        Elimina todo el historial de ventas del sistema.
        
        Returns:
            str: Mensaje confirmando la eliminación del historial
        """
        self.db.delete_all_sales()
        return "Historial de ventas borrado correctamente."
