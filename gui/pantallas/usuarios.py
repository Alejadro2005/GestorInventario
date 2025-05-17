"""
Módulo para la gestión integral de usuarios en el sistema.

Contiene las pantallas para:
- Menú principal de gestión de usuarios
- Creación de nuevos usuarios
- Eliminación de usuarios existentes
- Listado completo de usuarios registrados
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from src.modelos.usuario import Usuario


class UsuariosMenuScreen(Screen):
    """
    Pantalla principal para navegar por las operaciones de usuarios.

    Attributes:
        gestor (ObjectProperty): Conexión al gestor de usuarios
        console_ui (ObjectProperty): Conexión a la interfaz principal
    """
    gestor = ObjectProperty(None)
    console_ui = ObjectProperty(None)

    def on_pre_enter(self):
        """Verifica que el usuario tenga sesión de administrador antes de mostrar el menú."""
        try:
            if not hasattr(self.console_ui, 'usuario_actual') or not self.console_ui.usuario_actual:
                self.manager.current = 'login'
                return
            if self.console_ui.usuario_actual.rol != "admin":
                self.mostrar_popup("❌ Error", "Solo usuarios con rol ADMIN pueden acceder")
                self.manager.current = 'main'
        except Exception as e:
            self.mostrar_popup("❌ Error", str(e))
            self.manager.current = 'main'

    def mostrar_submenu(self, opcion: str):
        """
        Gestiona la navegación entre pantallas según la opción seleccionada.

        Args:
            opcion (str): Número de la opción del menú
        """
        self.manager.current = {
            '1': 'crear_usuario',
            '2': 'eliminar_usuario',
            '3': 'listar_usuarios',
            '4': 'main'
        }.get(opcion, 'main')

    def mostrar_popup(self, titulo: str, mensaje: str):
        """
        Muestra un mensaje emergente.

        Args:
            titulo (str): Título del popup
            mensaje (str): Contenido del mensaje
        """
        label = Label(
            text=mensaje,
            color=(0, 0, 0, 1),
            halign='left',
            valign='top',
            markup=True,
            text_size=(400, None),  # Ajusta el ancho máximo aquí
            size_hint_y=None
        )
        # Forzar el cálculo del alto del label
        label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        label.height = label.texture_size[1]

        popup = Popup(
            title=titulo,
            content=label,
            size_hint=(0.6, 0.5)  # Puedes aumentar el alto si lo deseas
        )
        popup.open()


class CrearUsuarioScreen(Screen):
    """
    Pantalla para el registro de nuevos usuarios en el sistema.

    Attributes:
        gestor (ObjectProperty): Conexión al gestor de usuarios
    """
    gestor = ObjectProperty(None)

    def on_pre_enter(self):
        """Prepara el formulario al entrar a la pantalla."""
        self.resetear_campos()

    def crear_usuario(self):
        """Valida y registra un nuevo usuario con los datos del formulario."""
        try:
            nombre = self.ids.nombre_usuario.text.strip()
            rol = self.ids.rol_usuario.text.strip().lower()
            password = self.ids.password_usuario.text.strip()

            if not nombre or not rol or not password:
                raise ValueError("Todos los campos son obligatorios")
            if len(password) < 6:
                raise ValueError("La contraseña debe tener al menos 6 caracteres")
            if rol not in ["admin", "empleado"]:
                raise ValueError("El rol debe ser 'admin' o 'empleado'")

            # El ID ya no se solicita, se pone un valor ficticio (0) solo para cumplir con la firma
            nuevo = Usuario(0, nombre, rol, password)
            self.gestor.crear_usuario(nuevo)
            self.mostrar_popup("✅ Éxito", "Usuario creado exitosamente!")
            self.manager.current = 'usuarios_menu'
        except Exception as e:
            self.mostrar_popup("❌ Error", str(e))
        finally:
            self.resetear_campos()

    def resetear_campos(self):
        """Reinicia todos los campos del formulario a valores vacíos."""
        for field in ['nombre_usuario', 'rol_usuario', 'password_usuario']:
            self.ids[field].text = ''

    def mostrar_popup(self, titulo: str, mensaje: str):
        """
        Muestra un mensaje emergente.

        Args:
            titulo (str): Título del popup
            mensaje (str): Contenido del mensaje
        """
        popup = Popup(
            title=titulo,
            content=Label(
                text=mensaje,
                color=(0, 0, 0, 1),
                halign='left',
                valign='middle',
                text_size=(400, None)  # Ajusta el ancho máximo aquí
            ),
            size_hint=(0.6, 0.4)
        )
        popup.open()


class EliminarUsuarioScreen(Screen):
    """
    Pantalla para eliminar usuarios del sistema.

    Attributes:
        gestor (ObjectProperty): Conexión al gestor de usuarios
    """
    gestor = ObjectProperty(None)

    def eliminar_usuario(self):
        """Elimina un usuario mediante su ID después de validación."""
        try:
            usuario_id = int(self.ids.id_eliminar.text.strip())
            self.gestor.eliminar_usuario(usuario_id)
            self.mostrar_popup("✅ Éxito", "Usuario eliminado correctamente")
            self.ids.id_eliminar.text = ""
            self.manager.current = 'usuarios_menu'
        except Exception as e:
            msg = str(e)
            if 'llave foránea' in msg or 'foreign key' in msg:
                self.mostrar_popup("❌ Error", "No se puede eliminar el usuario porque está asociado a ventas registradas.")
            else:
                self.mostrar_popup("❌ Error", msg)

    def mostrar_popup(self, titulo: str, mensaje: str):
        """
        Muestra un mensaje emergente.

        Args:
            titulo (str): Título del popup
            mensaje (str): Contenido del mensaje
        """
        popup = Popup(
            title=titulo,
            content=Label(
                text=mensaje,
                color=(0, 0, 0, 1),
                halign='left',
                valign='middle',
                text_size=(400, None)  # Ajusta el ancho máximo aquí
            ),
            size_hint=(0.6, 0.4)
        )
        popup.open()


class ListarUsuariosScreen(Screen):
    """
    Pantalla para visualizar el listado completo de usuarios registrados.

    Attributes:
        gestor (ObjectProperty): Conexión al gestor de usuarios
    """
    gestor = ObjectProperty(None)

    def on_pre_enter(self):
        """Prepara los datos de usuarios antes de mostrar la pantalla."""
        try:
            usuarios = self.gestor.db.get_all_users()
            self.ids.lista_usuarios.data = [{
                'texto': f"ID: {usuario['id']} | Nombre: {usuario['nombre']} | Rol: {usuario['rol'].capitalize()}"
            } for usuario in usuarios]
        except Exception as e:
            self.mostrar_popup("❌ Error", str(e))

    def mostrar_popup(self, titulo: str, mensaje: str):
        """
        Muestra un mensaje emergente.

        Args:
            titulo (str): Título del popup
            mensaje (str): Contenido del mensaje
        """
        popup = Popup(
            title=titulo,
            content=Label(
                text=mensaje,
                color=(0, 0, 0, 1),
                halign='left',
                valign='middle',
                text_size=(400, None)  # Ajusta el ancho máximo aquí
            ),
            size_hint=(0.6, 0.4)
        )
        popup.open()