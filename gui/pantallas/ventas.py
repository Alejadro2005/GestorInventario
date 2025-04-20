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
        self.ids.lista_productos.data = [{
            'text': f"{p.nombre} (ID: {p.id}) - ${p.precio:.2f}" + (" [Agotado]" if p.cantidad == 0 else "")
        } for p in self.inventario.productos]

    def agregar_producto_venta(self):
        """
        Agrega un producto a la lista de seleccionados para la venta actual.
        Realiza validaciones de stock, cantidad y duplicados.
        """
        try:
            # Obtener y validar datos de entrada
            producto_id = int(self.ids.id_producto.text)
            cantidad = int(self.ids.cantidad.text)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor a 0")

            # Buscar producto en el inventario
            producto = next(p for p in self.inventario.productos if p.id == producto_id)

            # Validar disponibilidad
            if producto.cantidad == 0:
                raise ValueError(f"{producto.nombre} está agotado")
            if cantidad > producto.cantidad:
                raise ValueError(f"Solo hay {producto.cantidad} unidades de {producto.nombre}")
            if any(p.id == producto.id for p, _ in self.productos_seleccionados):
                raise ValueError(f"{producto.nombre} ya fue agregado")

            # Agregar a la lista temporal de venta
            self.productos_seleccionados.append((producto, cantidad))
            self.actualizar_lista_seleccionados()

            # Limpiar campos y mostrar confirmación
            self.ids.id_producto.text = ""
            self.ids.cantidad.text = ""
            self.mostrar_popup("✅ Añadido", f"{producto.nombre} x{cantidad}")
        except Exception as e:
            self.mostrar_popup("❌ Error", str(e))

    def procesar_venta(self):
        """
        Registra una nueva venta en el sistema.
        Valida empleado, fecha y productos seleccionados.
        Actualiza inventario y guarda cambios.
        """
        try:
            if not self.productos_seleccionados:
                raise ValueError("Debe seleccionar al menos un producto")

            # Validar fecha y empleado
            fecha = self.validar_fecha(self.ids.fecha_venta.text)
            id_empleado = int(self.ids.id_empleado.text)
            usuario = self.console_ui.gestor.obtener_usuario(id_empleado)

            if usuario.rol != "empleado":
                raise ValueError("Solo empleados pueden registrar ventas")

            # Crear y registrar la venta
            venta = Venta(
                len(self.tienda.historial_ventas) + 1,
                fecha,
                self.productos_seleccionados,
                id_empleado,
                self.inventario
            )

            resultado = self.tienda.registrar_venta(venta, self.inventario)
            self.console_ui._guardar_inventario()  # Persistir cambios

            self.mostrar_popup("✅ Éxito", resultado)
            self.resetear_campos()
            self.manager.current = 'main'
        except Exception as e:
            self.mostrar_popup("❌ Error", str(e))

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
        self.ids.productos_seleccionados.data = [{'text': f"{p.nombre} x{cantidad}"}
                                                 for p, cantidad in self.productos_seleccionados]

    def mostrar_popup(self, titulo, mensaje):
        """
        Muestra un popup informativo.

        Args:
            titulo (str): Título del popup
            mensaje (str): Contenido del mensaje
        """
        Popup(title=titulo, content=Label(text=mensaje, color=(0, 0, 0, 1)), size_hint=(0.6, 0.4)).open()