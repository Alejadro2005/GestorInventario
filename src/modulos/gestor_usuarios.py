from src.modelos.usuario import Usuario
from src.errores.usuario_no_encontrado import UsuarioNoEncontradoError
from src.errores.usuario_duplicado import UsuarioDuplicadoError
from src.database.database_interface import DatabaseInterface

class GestorUsuarios:
    """
    Clase encargada de gestionar usuarios: creación, eliminación, validación y persistencia.

    Attributes:
        db (DatabaseInterface): Instancia de la interfaz de base de datos.
    """

    def __init__(self, db: DatabaseInterface):
        """
        Inicializa el gestor con una instancia de la base de datos.

        Args:
            db (DatabaseInterface): Instancia de la interfaz de base de datos.
        """
        self.db = db

    def crear_usuario(self, usuario: Usuario) -> str:
        """
        Crea un nuevo usuario en la base de datos.

        Args:
            usuario (Usuario): Objeto de tipo Usuario a registrar.

        Returns:
            str: Mensaje de confirmación.

        Raises:
            UsuarioDuplicadoError: Si ya existe un usuario con el mismo ID.
        """
        try:
            user_data = usuario.to_dict()
            user_data['password'] = user_data.pop('contraseña')
            self.db.create_user(user_data)
            return f"Usuario '{usuario.nombre}' creado con éxito."
        except Exception as e:
            if "UNIQUE constraint failed" in str(e):
                raise UsuarioDuplicadoError(f"El usuario con ID {usuario.id} ya existe.")
            raise e

    def eliminar_usuario(self, id_usuario: int) -> str:
        """
        Elimina un usuario dado su ID.

        Args:
            id_usuario (int): ID del usuario a eliminar.

        Returns:
            str: Mensaje de confirmación.

        Raises:
            UsuarioNoEncontradoError: Si el usuario no está registrado.
        """
        usuario = self.db.get_user(id_usuario)
        if not usuario:
            raise UsuarioNoEncontradoError(f"El usuario con ID {id_usuario} no existe.")
        
        if self.db.delete_user(id_usuario):
            return f"Usuario '{usuario['nombre']}' eliminado con éxito."
        raise UsuarioNoEncontradoError(f"El usuario con ID {id_usuario} no existe.")

    def obtener_usuario(self, id_usuario: int) -> Usuario:
        """
        Retorna un usuario dado su ID.

        Args:
            id_usuario (int): ID del usuario a buscar.

        Returns:
            Usuario: El usuario correspondiente al ID.

        Raises:
            UsuarioNoEncontradoError: Si el usuario no está registrado.
        """
        usuario = self.db.get_user(id_usuario)
        if not usuario:
            raise UsuarioNoEncontradoError(f"El usuario con ID {id_usuario} no existe.")
        usuario['contraseña'] = usuario.pop('password')
        usuario.pop('fecha_creacion', None)
        return Usuario(**usuario)

    def validar_rol(self, id_usuario: int, rol_requerido: str) -> bool:
        """
        Verifica si un usuario tiene un rol específico.

        Args:
            id_usuario (int): ID del usuario a validar.
            rol_requerido (str): Rol que se desea comprobar.

        Returns:
            bool: True si el usuario tiene el rol requerido, False en caso contrario.
        """
        usuario = self.db.get_user(id_usuario)
        if not usuario:
            raise UsuarioNoEncontradoError(f"El usuario con ID {id_usuario} no existe.")
        return usuario['rol'] == rol_requerido
