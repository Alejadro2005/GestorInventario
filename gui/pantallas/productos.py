"""
Módulo para la gestión completa de productos en el sistema.

Contiene las pantallas para:
- Menú de gestión de productos
- Agregar nuevos productos
- Eliminar productos existentes
- Actualizar niveles de stock
- Visualización detallada del inventario
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from src.modelos.producto import Producto


class ProductosMenuScreen(Screen):
    """
    Pantalla principal para navegar por las operaciones de productos.

    Attributes:
        console_ui (ObjectProperty): Conexión con la interfaz principal
    """
    console_ui = ObjectProperty(None)

    def mostrar_submenu(self, opcion):
        """
        Gestiona la navegación entre pantallas según la opción seleccionada.

        Args:
            opcion (str): Número de la opción del menú
        """
        self.manager.current = {
            '1': 'agregar_producto',
            '2': 'eliminar_producto',
            '3': 'actualizar_stock',
            '4': 'ver_inventario',
            '5': 'main'
        }.get(opcion, 'main')


class AgregarProductoScreen(Screen):
    """
    Pantalla para registrar nuevos productos en el inventario.

    Attributes:
        inventario (ObjectProperty): Conexión al módulo de inventario
        console_ui (ObjectProperty): Enlace a la interfaz principal
    """
    inventario = ObjectProperty(None)
    console_ui = ObjectProperty(None)

    def agregar_producto(self):
        """Valida y registra un nuevo producto con los datos del formulario."""
        try:
            categoria = self.ids.categoria_producto.text.lower()
            if categoria not in ['electronica', 'escolar']:
                raise ValueError("Categoría debe ser 'electronica' o 'escolar'")
            nuevo = Producto(
                int(self.ids.id_producto.text),
                self.ids.nombre_producto.text,
                float(self.ids.precio_producto.text),
                int(self.ids.cantidad_producto.text),
                categoria,
                int(self.ids.stock_minimo.text)
            )
            self.inventario.agregar_producto(nuevo)
            self.console_ui._guardar_inventario()
            self.mostrar_popup("✅ Éxito", "Producto agregado correctamente!")
            self.resetear_campos()
            self.manager.current = 'productos_menu'
        except Exception as e:
            self.mostrar_popup("❌ Error", str(e))

    def resetear_campos(self):
        """Reinicia todos los campos del formulario a valores vacíos."""
        for field in ['id_producto', 'nombre_producto', 'precio_producto',
                      'cantidad_producto', 'categoria_producto', 'stock_minimo']:
            self.ids[field].text = ''

    def mostrar_popup(self, titulo, mensaje):
        """
        Muestra un mensaje emergente.

        Args:
            titulo (str): Título del popup
            mensaje (str): Contenido del mensaje
        """
        Popup(title=titulo, content=Label(text=mensaje, color=(0, 0, 0, 1)), size_hint=(0.6, 0.4)).open()


class EliminarProductoScreen(Screen):
    """
    Pantalla para eliminar productos del inventario.

    Attributes:
        inventario (ObjectProperty): Conexión al módulo de inventario
        console_ui (ObjectProperty): Enlace a la interfaz principal
    """
    inventario = ObjectProperty(None)
    console_ui = ObjectProperty(None)

    def eliminar_producto(self):
        """Elimina un producto del sistema mediante su ID."""
        try:
            producto_id = int(self.ids.id_eliminar.text)
            resultado = self.inventario.eliminar_producto(producto_id)
            self.console_ui._guardar_inventario()
            self.mostrar_popup("✅ Éxito", resultado)
            self.ids.id_eliminar.text = ""
            self.manager.current = 'productos_menu'
        except Exception as e:
            self.mostrar_popup("❌ Error", str(e))

    def mostrar_popup(self, titulo, mensaje):
        """
        Muestra un mensaje emergente.

        Args:
            titulo (str): Título del popup
            mensaje (str): Contenido del mensaje
        """
        Popup(title=titulo, content=Label(text=mensaje, color=(0, 0, 0, 1)), size_hint=(0.6, 0.4)).open()


class ActualizarStockScreen(Screen):
    """
    Pantalla para modificar las existencias de productos.

    Attributes:
        inventario (ObjectProperty): Conexión al módulo de inventario
        console_ui (ObjectProperty): Enlace a la interfaz principal
    """
    inventario = ObjectProperty(None)
    console_ui = ObjectProperty(None)

    def actualizar_stock(self):
        """Actualiza la cantidad disponible de un producto en el inventario."""
        try:
            producto_id = int(self.ids.id_producto.text.strip())
            nueva_cantidad = int(self.ids.nueva_cantidad.text.strip())
            resultado = self.inventario.actualizar_stock(producto_id, nueva_cantidad)
            self.console_ui._guardar_inventario()
            self.mostrar_popup("✅ Éxito", resultado)
            self.ids.id_producto.text = ""
            self.ids.nueva_cantidad.text = ""
            self.manager.current = 'productos_menu'
        except Exception as e:
            self.mostrar_popup("❌ Error", str(e))

    def mostrar_popup(self, titulo, mensaje):
        """
        Muestra un mensaje emergente.

        Args:
            titulo (str): Título del popup
            mensaje (str): Contenido del mensaje
        """
        Popup(title=titulo, content=Label(text=mensaje, color=(0, 0, 0, 1)), size_hint=(0.6, 0.4)).open()


class VerInventarioScreen(Screen):
    """
    Pantalla para visualizar el inventario completo con detalles de productos.

    Attributes:
        inventario (ObjectProperty): Conexión al módulo de inventario
    """
    inventario = ObjectProperty(None)

    def on_pre_enter(self):
        """Prepara los datos del inventario antes de mostrar la pantalla."""
        self.ids.lista_productos.data = [{
            'texto_inventario': f"""[b]🆔 ID:[/b] {p.id}
            [b]📦 Producto:[/b] {p.nombre[:20] + "..." if len(p.nombre) > 20 else p.nombre}
            [b]💲 Precio:[/b] ${p.precio:.2f}
            [b]📥 Stock:[/b] {p.cantidad} unidades
            [b]🚨 Mínimo requerido:[/b] {p.stock_minimo}
            [b]📂 Categoría:[/b] {p.categoria[:10] + "..." if len(p.categoria) > 10 else p.categoria}
            ───────────────────────────"""
        } for p in self.inventario.productos]