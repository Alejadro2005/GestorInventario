from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, ListProperty
from datetime import datetime
from src.modelos.venta import Venta


class VentasScreen(Screen):
    """
    Pantalla para gestionar el proceso de ventas y registro de transacciones.

    Attributes:
        inventario (ObjectProperty): Conexión al inventario de productos
        tienda (ObjectProperty): Conexión a la instancia de la tienda
        console_ui (ObjectProperty): Referencia a la interfaz principal
        productos_seleccionados (ListProperty): Lista de productos seleccionados para la venta actual
    """
    inventario = ObjectProperty(None)
    tienda = ObjectProperty(None)
    console_ui = ObjectProperty(None)
    productos_seleccionados = ListProperty([])

    def on_pre_enter(self):
        """Inicializa los campos al entrar a la pantalla"""
        self.resetear_campos()

    def cargar_productos_disponibles(self):
        """Actualiza la lista de productos mostrada con stock actual y estados"""
        productos = self.inventario.db.get_all_products()
        self.ids.lista_productos.data = [{
            'texto_producto': f"{p['nombre']} (ID: {p['id']}) - {int(p['precio']):,} - Stock: {p['cantidad']}" + (" [Agotado]" if p['cantidad'] == 0 else ""),
            'id_producto': p['id']
        } for p in productos]

    def agregar_producto_venta(self):
        """
        Agrega un producto a la lista de seleccionados para la venta actual.
        Realiza validaciones de stock, cantidad y duplicados.
        """
        try:
            # Validar campos vacíos
            if not self.ids.id_producto.text or not self.ids.cantidad.text:
                raise ValueError("Debe ingresar ID y cantidad del producto")

            # Obtener y validar datos de entrada
            producto_id = int(self.ids.id_producto.text)
            cantidad = int(self.ids.cantidad.text)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")

            # Buscar producto en la base de datos
            producto = self.inventario.db.get_product(producto_id)
            if not producto:
                raise ValueError(f"No se encontró un producto con ID {producto_id}")

            # Validar disponibilidad
            if producto['cantidad'] == 0:
                raise ValueError(f"{producto['nombre']} está agotado")
            if cantidad > producto['cantidad']:
                raise ValueError(f"Solo hay {producto['cantidad']} unidades de {producto['nombre']}")
            
            # Verificar si el producto ya está en la lista
            for p, _ in self.productos_seleccionados:
                if p['id'] == producto['id']:
                    raise ValueError(f"{producto['nombre']} ya fue agregado")

            # Agregar a la lista temporal de venta
            self.productos_seleccionados.append((producto, cantidad))
            self.actualizar_lista_seleccionados()

            # Limpiar campos y mostrar confirmación
            self.ids.id_producto.text = ""
            self.ids.cantidad.text = ""
            self.mostrar_popup("✅ Añadido", f"{producto['nombre']} x{cantidad}")
        except ValueError as e:
            self.mostrar_popup("❌ Error", str(e))
        except Exception as e:
            self.mostrar_popup("❌ Error", "Error inesperado al agregar el producto")

    def procesar_venta(self):
        """
        Registra una nueva venta en el sistema.
        Valida empleado, fecha y productos seleccionados.
        Actualiza inventario y guarda cambios.
        """
        import traceback
        try:
            # Validar campos obligatorios
            if not self.ids.id_empleado.text:
                raise ValueError("Debe ingresar el ID del empleado")
            if not self.ids.fecha_venta.text:
                raise ValueError("Debe ingresar la fecha de la venta")
            if not self.productos_seleccionados:
                raise ValueError("Debe seleccionar al menos un producto")

            # Validar fecha y empleado
            fecha = self.validar_fecha(self.ids.fecha_venta.text)
            id_empleado = int(self.ids.id_empleado.text)
            usuario = self.console_ui.gestor.obtener_usuario(id_empleado)

            if usuario.rol != "empleado":
                raise ValueError("Solo empleados pueden registrar ventas")

            # Validar stock antes de procesar la venta
            productos_a_eliminar = []
            for producto, cantidad in self.productos_seleccionados:
                producto_actual = self.inventario.db.get_product(producto['id'])
                if not producto_actual:
                    productos_a_eliminar.append((producto, cantidad))
                    continue
                if producto_actual['cantidad'] < cantidad:
                    self.mostrar_popup(
                        "Stock insuficiente",
                        f"Stock insuficiente para {producto['nombre']}. Disponible: {producto_actual['cantidad']}, requerido: {cantidad}.\nReduzca la cantidad o actualice el stock antes de procesar la venta."
                    )
                    return
            # Eliminar productos no disponibles
            if productos_a_eliminar:
                for p in productos_a_eliminar:
                    self.productos_seleccionados.remove(p)
                self.actualizar_lista_seleccionados()
                self.mostrar_popup(
                    "Producto no disponible",
                    "Uno o más productos ya no existen en el inventario y han sido eliminados de la venta."
                )
                return

            # Calcular el nuevo ID de venta usando la base de datos
            nuevo_id = self.tienda.db.get_next_sale_id()

            # Crear y registrar la venta
            from src.errores.stock_insuficiente import StockInsuficienteError
            from src.errores.venta_producto_no_registrado import VentaProductoNoRegistradoError
            from src.errores.venta_invalida import VentaInvalidaError
            from src.errores.fecha_invalida import FechaInvalidaError
            from src.errores.venta_sin_empleado import VentaSinEmpleadoError
            try:
                venta = Venta(
                    nuevo_id,
                    fecha,
                    self.productos_seleccionados,
                    id_empleado,
                    self.inventario
                )
                resultado = self.tienda.registrar_venta(venta, self.inventario)
            except StockInsuficienteError as e:
                self.mostrar_popup("Stock insuficiente", str(e) + "\nReduzca la cantidad o actualice el stock.")
                return
            except VentaProductoNoRegistradoError as e:
                self.mostrar_popup("Producto no registrado", str(e) + "\nActualice el inventario.")
                return
            except VentaInvalidaError as e:
                self.mostrar_popup("Venta inválida", str(e))
                return
            except FechaInvalidaError as e:
                self.mostrar_popup("Fecha inválida", str(e))
                return
            except VentaSinEmpleadoError as e:
                self.mostrar_popup("Empleado inválido", str(e))
                return
            except Exception as e:
                traceback.print_exc()
                self.mostrar_popup("Error inesperado", f"Ocurrió un error inesperado: {type(e).__name__}: {e}")
                return

            # Verificar que el stock se actualizó correctamente
            for producto, cantidad in self.productos_seleccionados:
                producto_actual = self.inventario.db.get_product(producto['id'])
                if producto_actual['cantidad'] != producto['cantidad'] - cantidad:
                    self.mostrar_popup("Error de stock", f"Error al actualizar el stock de {producto['nombre']}")
                    return

            self.mostrar_popup("Éxito", "Venta realizada")
            self.resetear_campos()
            self.manager.current = 'main'
        except ValueError as e:
            self.mostrar_popup("Error", str(e))
        except Exception as e:
            traceback.print_exc()
            self.mostrar_popup("Error inesperado", f"Ocurrió un error inesperado: {type(e).__name__}: {e}")

    def validar_fecha(self, fecha_str):
        """
        Valida y formatea una cadena de fecha.

        Args:
            fecha_str (str): Fecha en formato DD/MM/AAAA o DD/MM/AA

        Returns:
            str: Fecha formateada como DD/MM/AAAA

        Raises:
            ValueError: Si el formato es inválido
        """
        try:
            day, month, year = map(int, fecha_str.split('/'))
            # Manejar años en formato corto (YY)
            if len(str(year)) == 2:
                year += 2000
            datetime(year, month, day)  # Validación de fecha real
            return f"{day:02d}/{month:02d}/{year}"
        except:
            raise ValueError("Formato de fecha inválido (DD/MM/AAAA)")

    def resetear_campos(self):
        """Reinicia todos los campos a sus valores iniciales"""
        self.productos_seleccionados = []
        self.ids.fecha_venta.text = datetime.now().strftime("%d/%m/%Y")
        self.ids.id_empleado.text = ""
        self.ids.id_producto.text = ""
        self.ids.cantidad.text = ""
        self.actualizar_lista_seleccionados()
        self.cargar_productos_disponibles()

    def actualizar_lista_seleccionados(self):
        """Actualiza la interfaz con los productos seleccionados"""
        self.ids.productos_seleccionados.data = [{'text': f"{p['nombre']} x{cantidad}"}
                                                 for p, cantidad in self.productos_seleccionados]
        
        # Actualizar resumen de la venta
        if self.productos_seleccionados:
            total = sum(p['precio'] * cantidad for p, cantidad in self.productos_seleccionados)
            self.ids.resumen_venta.text = f"Total de la venta: {int(total):,}"
        else:
            self.ids.resumen_venta.text = ""

    def mostrar_popup(self, titulo, mensaje):
        """
        Muestra un popup informativo.

        Args:
            titulo (str): Título del popup
            mensaje (str): Contenido del mensaje
        """
        Popup(title=titulo, content=Label(text=str(mensaje), color=(0, 0, 0, 1)), size_hint=(0.6, 0.4)).open()

    def seleccionar_producto(self, id_producto):
        """Rellena el campo de ID de producto con el seleccionado."""
        self.ids.id_producto.text = str(id_producto)