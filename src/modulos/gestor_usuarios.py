from modelos.usuario import Usuario
from errores.usuario_no_encontrado import UsuarioNoEncontradoError
from errores.usuario_duplicado import UsuarioDuplicadoError
from database.database_interface import DatabaseInterface
import logging
from typing import List
from errores.contrasena_invalida import ContrasenaInvalidaError

logger = logging.getLogger(__name__)

class GestorUsuarios:
    """
    Clase que gestiona las operaciones relacionadas con los usuarios del sistema.
    
    Esta clase permite crear, obtener, actualizar y eliminar usuarios, así como validar credenciales y roles.

    Attributes:
        db: Instancia de la base de datos utilizada para persistencia
    """

    def __init__(self, db: DatabaseInterface):
        """
        Inicializa el gestor de usuarios con una instancia de base de datos.

        Args:
            db: Instancia de la base de datos
        """
        self.db = db

    def crear_usuario(self, usuario: Usuario) -> int:
        """
        Crea un nuevo usuario en el sistema.

        Args:
            usuario (Usuario): Usuario a crear

        Returns:
            int: ID del usuario creado
        """
        usuario_dict = usuario.to_dict()
        # Adaptar clave para la base de datos
        if 'contraseña' in usuario_dict:
            usuario_dict['password'] = usuario_dict.pop('contraseña')
        return self.db.create_user(usuario_dict)

    def obtener_usuario(self, id_usuario: int) -> Usuario:
        """
        Obtiene un usuario por su ID.

        Args:
            id_usuario (int): ID del usuario

        Returns:
            Usuario o None si no existe
        """
        data = self.db.get_user(id_usuario)
        if data:
            return Usuario.from_dict(data)
        return None

    def actualizar_usuario(self, id_usuario: int, usuario: Usuario) -> bool:
        """
        Actualiza los datos de un usuario existente.
        
        Args:
            id_usuario (int): ID del usuario a actualizar
            usuario (Usuario): Nuevos datos del usuario
        
        Returns:
            bool: True si se actualizó correctamente
        """
        return self.db.update_user(id_usuario, usuario.to_dict())

    def eliminar_usuario(self, id_usuario: int) -> bool:
        """
        Elimina un usuario del sistema por su ID.

        Args:
            id_usuario (int): ID del usuario a eliminar

        Returns:
            bool: True si se eliminó correctamente
        """
        return self.db.delete_user(id_usuario)

    def obtener_todos_usuarios(self) -> List[Usuario]:
        """
        Retorna una lista de todos los usuarios registrados.
        
        Returns:
            list: Lista de instancias de Usuario
        """
        usuarios_data = self.db.get_all_users()
        return [Usuario.from_dict(u) for u in usuarios_data]

    def validar_credenciales(self, id_usuario: int, password: str) -> bool:
        """
        Valida las credenciales de un usuario.
        
        Args:
            id_usuario (int): ID del usuario
            password (str): Contraseña a validar
        
        Returns:
            bool: True si las credenciales son válidas
        """
        usuario = self.obtener_usuario(id_usuario)
        if usuario and usuario.password == password:
            return True
        return False

    def validar_rol(self, id_usuario: int, rol_requerido: str) -> bool:
        """
        Verifica si un usuario tiene un rol específico.

        Args:
            id_usuario (int): ID del usuario a validar.
            rol_requerido (str): Rol que se desea comprobar.

        Returns:
            bool: True si el usuario tiene el rol requerido, False en caso contrario.

        Raises:
            UsuarioNoEncontradoError: Si el usuario no está registrado.
        """
        usuario = self.obtener_usuario(id_usuario)
        if not usuario:
            raise UsuarioNoEncontradoError(f"El usuario con ID {id_usuario} no existe.")
        return usuario.rol == rol_requerido

    def actualizar_cache(self):
        """
        Actualiza el caché de usuarios con los datos más recientes de la base de datos.
        """
        try:
            usuarios_db = self.db.get_all_users()
            self.usuarios = {u['id']: Usuario.from_dict(u) for u in usuarios_db}
            logger.info("Caché de usuarios actualizado correctamente")
        except Exception as e:
            logger.error(f"Error al actualizar caché de usuarios: {str(e)}")
            raise
