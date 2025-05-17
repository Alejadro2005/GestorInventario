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
    """

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
    """
    inventario = ObjectProperty(None)

    def agregar_producto(self):
        """Valida y registra un nuevo producto con los datos del formulario."""
        try:
            categoria = self.ids.categoria_producto.text.lower()
            if categoria not in ['electronica', 'escolar']:
                raise ValueError("Categoría debe ser 'electronica' o 'escolar'")
            # Usar id ficticio (0) ya que la base de datos lo asigna automáticamente
            nuevo = Producto(
                0,  # id ficticio, ignorado por la base de datos
                self.ids.nombre_producto.text,
                float(self.ids.precio_producto.text),
                int(self.ids.cantidad_producto.text),
                categoria,
                int(self.ids.stock_minimo.text)
            )
            self.inventario.agregar_producto(nuevo)
            self.mostrar_popup("✅ Éxito", "Producto agregado correctamente!")
            self.resetear_campos()
            self.manager.current = 'productos_menu'
        except Exception as e:
            self.mostrar_popup("❌ Error", str(e))

    def resetear_campos(self):
        """Reinicia todos los campos del formulario a valores vacíos."""
        for field in ['nombre_producto', 'precio_producto',
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
    """
    inventario = ObjectProperty(None)

    def on_pre_enter(self):
        """Carga la lista de productos al entrar en la pantalla."""
        productos = self.inventario.db.get_all_products()
        self.ids.lista_productos_eliminar.data = [
            {
                'texto_producto': f"🆔 {p['id']} | {p['nombre'][:25] + '...' if len(p['nombre']) > 25 else p['nombre']}",
                'id_producto': p['id']
            }
            for p in productos
        ]

    def seleccionar_producto(self, id_producto):
        """Rellena el campo de ID con el producto seleccionado."""
        self.ids.id_eliminar.text = str(id_producto)

    def eliminar_producto(self):
        """Elimina un producto del sistema mediante su ID."""
        try:
            producto_id = int(self.ids.id_eliminar.text)
            resultado = self.inventario.eliminar_producto(producto_id)
            self.mostrar_popup("✅ Éxito", resultado)
            self.ids.id_eliminar.text = ""
            self.manager.current = 'productos_menu'
        except Exception as e:
            msg = str(e)
            if 'llave foránea' in msg or 'foreign key' in msg:
                self.mostrar_popup("❌ Error", "No se puede eliminar el producto porque está asociado a ventas registradas.")
            else:
                self.mostrar_popup("❌ Error", msg)

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
    """
    inventario = ObjectProperty(None)

    def on_pre_enter(self):
        """Carga la lista de productos al entrar en la pantalla."""
        self.cargar_productos()

    def cargar_productos(self):
        """Carga la lista de productos en el RecycleView"""
        try:
            # Obtener la lista de productos
            productos = self.inventario.db.get_all_products()
            
            # Crear la lista de datos para el RecycleView
            data = []
            for producto in productos:
                data.append({
                    'texto_producto': f"{producto['id']} - {producto['nombre']} (Stock: {producto['cantidad']})",
                    'id_producto': producto['id']
                })
            
            # Actualizar el RecycleView
            self.ids.lista_productos_actualizar.data = data
        except Exception as e:
            print(f"Error al cargar productos: {str(e)}")

    def seleccionar_producto(self, id_producto):
        """Maneja la selección de un producto de la lista"""
        self.ids.id_producto.text = str(id_producto)
        # Obtener el stock actual del producto
        try:
            producto = self.inventario.db.get_product(id_producto)
            if producto:
                self.ids.nueva_cantidad.text = str(producto['cantidad'])
        except Exception as e:
            print(f"Error al obtener producto: {str(e)}")

    def actualizar_stock(self):
        """Actualiza el stock del producto seleccionado"""
        try:
            if not self.ids.id_producto.text:
                self.mostrar_popup("❌ Error", "Debe seleccionar un producto primero")
                return
                
            id_producto = int(self.ids.id_producto.text)
            nueva_cantidad = int(self.ids.nueva_cantidad.text)
            
            if nueva_cantidad < 0:
                raise ValueError("La cantidad no puede ser negativa")
            
            # Actualizar el stock
            self.inventario.actualizar_stock(id_producto, nueva_cantidad)
            
            # Mostrar mensaje de éxito
            self.mostrar_popup("✅ Éxito", f"Stock actualizado exitosamente para el producto {id_producto}")
            
            # Limpiar campos
            self.ids.id_producto.text = ''
            self.ids.nueva_cantidad.text = ''
            
            # Recargar la lista de productos
            self.cargar_productos()
            
        except ValueError as e:
            self.mostrar_popup("❌ Error", str(e))
        except Exception as e:
            self.mostrar_popup("❌ Error", f"Error al actualizar stock: {str(e)}")

    def sumar_stock(self):
        """Suma la cantidad indicada al stock actual del producto seleccionado."""
        try:
            if not self.ids.id_producto.text:
                self.mostrar_popup("❌ Error", "Debe seleccionar un producto primero")
                return

            id_producto = int(self.ids.id_producto.text)
            cantidad = int(self.ids.nueva_cantidad.text)
            if cantidad < 0:
                raise ValueError("La cantidad a sumar debe ser positiva")
            producto = self.inventario.db.get_product(id_producto)
            if not producto:
                raise ValueError("Producto no encontrado")
            nuevo_stock = producto['cantidad'] + cantidad
            self.inventario.actualizar_stock(id_producto, nuevo_stock)
            self.mostrar_popup("✅ Éxito", f"Stock sumado exitosamente. Nuevo stock: {nuevo_stock}")
            self.ids.id_producto.text = ''
            self.ids.nueva_cantidad.text = ''
            self.cargar_productos()
        except ValueError as e:
            self.mostrar_popup("❌ Error", str(e))
        except Exception as e:
            self.mostrar_popup("❌ Error", f"Error al sumar stock: {str(e)}")

    def restar_stock(self):
        """Resta la cantidad indicada al stock actual del producto seleccionado, sin permitir negativos."""
        try:
            if not self.ids.id_producto.text:
                self.mostrar_popup("❌ Error", "Debe seleccionar un producto primero")
                return

            id_producto = int(self.ids.id_producto.text)
            cantidad = int(self.ids.nueva_cantidad.text)
            if cantidad < 0:
                raise ValueError("La cantidad a restar debe ser positiva")
            producto = self.inventario.db.get_product(id_producto)
            if not producto:
                raise ValueError("Producto no encontrado")
            nuevo_stock = producto['cantidad'] - cantidad
            if nuevo_stock < 0:
                raise ValueError("El stock no puede quedar negativo")
            self.inventario.actualizar_stock(id_producto, nuevo_stock)
            self.mostrar_popup("✅ Éxito", f"Stock restado exitosamente. Nuevo stock: {nuevo_stock}")
            self.ids.id_producto.text = ''
            self.ids.nueva_cantidad.text = ''
            self.cargar_productos()
        except ValueError as e:
            self.mostrar_popup("❌ Error", str(e))
        except Exception as e:
            self.mostrar_popup("❌ Error", f"Error al restar stock: {str(e)}")

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
        productos = self.inventario.db.get_all_products()
        print(f"[DEBUG] Productos obtenidos en inventario: {productos}")
        self.ids.lista_productos.data = [{
            'texto_inventario': f"""[b]🆔 ID:[/b] {p['id']}
            [b]📦 Producto:[/b] {p['nombre'][:20] + '...' if len(p['nombre']) > 20 else p['nombre']}
            [b]💲 Precio:[/b] {int(p['precio']):,}
            [b]📥 Stock:[/b] {p['cantidad']} unidades
            [b]🚨 Mínimo requerido:[/b] {p['stock_minimo']}
            [b]📂 Categoría:[/b] {p['categoria'][:10] + '...' if len(p['categoria']) > 10 else p['categoria']}
            ───────────────────────────"""
        } for p in productos]