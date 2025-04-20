"""
Módulo que contiene componentes base y pantallas esenciales de la aplicación.

Incluye widgets personalizados y pantallas principales reutilizables.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label


class HistorialVentaItemCustom(BoxLayout):
    """
    Widget personalizado para mostrar elementos del historial de ventas.

    Attributes:
        texto_venta (StringProperty): Texto formateado con detalles de la venta
    """
    texto_venta = StringProperty("")


class ItemInventarioCustom(BoxLayout):
    """
    Widget personalizado para mostrar elementos del inventario.

    Attributes:
        texto_inventario (StringProperty): Texto formateado con detalles del producto
    """
    texto_inventario = StringProperty("")


class MainScreen(Screen):
    """Pantalla principal de la aplicación (contiene la navegación básica)."""
    pass


class LoginScreen(Screen):
    """
    Pantalla de autenticación para usuarios administrativos.

    Methods:
        verificar_credenciales: Valida usuario y contraseña
        mostrar_popup: Muestra mensajes emergentes
    """

    def verificar_credenciales(self):
        """Valida las credenciales de acceso contra el gestor de usuarios."""
        try:
            id_usuario = int(self.ids.id_usuario.text.strip())
            password = self.ids.password.text.strip()
            usuario = self.console_ui.gestor.obtener_usuario(id_usuario)

            if usuario.rol != "admin":
                raise ValueError("Solo usuarios con rol ADMIN pueden ingresar")
            usuario.iniciar_sesion(password)
            self.manager.current = 'productos_menu'
        except Exception as e:
            self.mostrar_popup("❌ Error de Login", str(e))

    def mostrar_popup(self, titulo: str, mensaje: str):
        """
        Muestra un mensaje emergente con información al usuario.

        Args:
            titulo (str): Título del popup
            mensaje (str): Contenido del mensaje
        """
        Popup(title=titulo, content=Label(text=mensaje, color=(0, 0, 0, 1)), size_hint=(0.6, 0.4)).open()