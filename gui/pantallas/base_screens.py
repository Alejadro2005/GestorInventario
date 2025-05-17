"""
Módulo que contiene componentes base y pantallas esenciales de la aplicación.

Incluye widgets personalizados y pantallas principales reutilizables.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from src.utils.logger import logger
import traceback


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


class BaseScreen(Screen):
    """
    Clase base para todas las pantallas con funcionalidad común.
    """
    console_ui = ObjectProperty(None)

    def sincronizar_estado(self):
        """
        Sincroniza el estado de la aplicación con la base de datos.
        """
        try:
            if hasattr(self.console_ui, 'inventario'):
                self.console_ui.inventario.actualizar_cache()
            if hasattr(self.console_ui, 'gestor'):
                self.console_ui.gestor.actualizar_cache()
            logger.info("Estado sincronizado correctamente")
        except Exception as e:
            logger.error(f"Error al sincronizar estado: {str(e)}")
            self.mostrar_popup("Error", "No se pudo sincronizar el estado")

    def mostrar_popup(self, titulo: str, mensaje: str, error: Exception = None):
        """
        Muestra un mensaje emergente solo con el mensaje amigable.
        Si hay error, lo loguea pero no lo muestra al usuario.
        """
        try:
            if error:
                logger.error(f"Error en {titulo}: {str(error)}\n{traceback.format_exc()}")
            label = Label(
                text=mensaje,
                color=(0, 0, 0, 1),
                halign='left',
                valign='top',
                markup=True,
                text_size=(400, None),
                size_hint_y=None
            )
            label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
            label.height = label.texture_size[1]
            popup = Popup(
                title=titulo,
                content=label,
                size_hint=(0.6, 0.5)
            )
            popup.open()
            logger.info(f"Popup mostrado: {titulo}")
        except Exception as e:
            logger.error(f"Error al mostrar popup: {str(e)}")
            Popup(title="Error", content=Label(text=str(e))).open()


class MainScreen(BaseScreen):
    """Pantalla principal de la aplicación."""
    pass


class LoginScreen(BaseScreen):
    """
    Pantalla de autenticación para usuarios administrativos.

    Methods:
        verificar_credenciales: Valida usuario y contraseña
        mostrar_popup: Muestra mensajes emergentes
    """
    destino = StringProperty('usuarios_menu')  # Por defecto va a usuarios_menu

    def verificar_credenciales(self):
        """Valida las credenciales de acceso contra el gestor de usuarios."""
        try:
            id_usuario = int(self.ids.id_usuario.text.strip())
            password = self.ids.password.text.strip()
            
            logger.info(f"Intento de login para usuario ID: {id_usuario}")
            
            usuario = self.console_ui.gestor.obtener_usuario(id_usuario)

            if usuario.rol != "admin":
                raise ValueError("Solo usuarios con rol ADMIN pueden ingresar")
                
            usuario.iniciar_sesion(password)
            self.console_ui.usuario_actual = usuario
            
            logger.info(f"Login exitoso para usuario: {usuario.nombre}")
            
            self.manager.current = self.destino
            self.sincronizar_estado()
            
        except Exception as e:
            logger.error(f"Error en login: {str(e)}")
            self.mostrar_popup("❌ Error de Login", "Credenciales incorrectas. Intente nuevamente.")