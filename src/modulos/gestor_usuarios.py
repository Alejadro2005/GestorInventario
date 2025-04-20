from src.modelos.usuario import Usuario
from src.errores.usuario_no_encontrado import UsuarioNoEncontradoError
from src.errores.usuario_duplicado import UsuarioDuplicadoError
from src.modulos.persistencia import ruta_absoluta
from src.modulos.persistencia import PersistenciaJSON
RUTA_USUARIOS = "data/usuarios.json"

class GestorUsuarios:
    """
    Clase encargada de gestionar usuarios: creación, eliminación, validación y persistencia.

    Attributes:
        usuarios (dict): Diccionario con usuarios cargados, con clave igual al ID del usuario.
    """

    def __init__(self, ruta_usuarios=RUTA_USUARIOS):
        """
        Inicializa el gestor cargando los usuarios desde un archivo JSON.

        Args:
            ruta_usuarios (str, optional): Ruta al archivo JSON donde están los usuarios.
                Por defecto es `RUTA_USUARIOS`.

        Side effects:
            Muestra mensajes de error si hay problemas al cargar usuarios mal formateados.
        """
        self.usuarios = {}

        ruta_resuelta = ruta_absoluta(ruta_usuarios)
        datos = PersistenciaJSON.cargar_datos(ruta_resuelta)

        for u in datos:
            try:
                if "_contraseña" in u:
                    u["contraseña"] = u.pop("_contraseña")

                usuario = Usuario(
                    id=u["id"],
                    nombre=u["nombre"],
                    rol=u["rol"],
                    contraseña=u["contraseña"]
                )
                self.usuarios[usuario.id] = usuario
            except KeyError as e:
                print(f"Error cargando usuario ID {u.get('id')}: Falta el campo {e}")
            except Exception as e:
                print(f"Error inesperado con usuario ID {u.get('id')}: {str(e)}")

    def crear_usuario(self, usuario: Usuario):
        """
        Crea un nuevo usuario y lo guarda en el archivo.

        Args:
            usuario (Usuario): Objeto de tipo Usuario a registrar.

        Returns:
            str: Mensaje de confirmación.

        Raises:
            UsuarioDuplicadoError: Si ya existe un usuario con el mismo ID.
        """
        if usuario.id in self.usuarios:
            raise UsuarioDuplicadoError(f"El usuario con ID {usuario.id} ya existe.")
        self.usuarios[usuario.id] = usuario
        self.guardar_usuarios()
        return f"Usuario '{usuario.nombre}' creado con éxito."

    def guardar_usuarios(self):
        """
        Guarda todos los usuarios actuales en el archivo JSON correspondiente.
        """
        datos = [u.to_dict() for u in self.usuarios.values()]
        PersistenciaJSON.guardar_datos(RUTA_USUARIOS, datos)

    def eliminar_usuario(self, id_usuario: int):
        """
        Elimina un usuario dado su ID y actualiza el archivo JSON.

        Args:
            id_usuario (int): ID del usuario a eliminar.

        Returns:
            str: Mensaje de confirmación.

        Raises:
            UsuarioNoEncontradoError: Si el usuario no está registrado.
        """
        if id_usuario not in self.usuarios:
            raise UsuarioNoEncontradoError(f"El usuario con ID {id_usuario} no existe.")
        nombre = self.usuarios[id_usuario].nombre
        del self.usuarios[id_usuario]
        self.guardar_usuarios()
        return f"Usuario '{nombre}' eliminado con éxito."

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
        if id_usuario not in self.usuarios:
            raise UsuarioNoEncontradoError(f"El usuario con ID {id_usuario} no existe.")
        return self.usuarios[id_usuario]

    def validar_rol(self, id_usuario: int, rol_requerido: str) -> bool:
        """
        Verifica si un usuario tiene un rol específico.

        Args:
            id_usuario (int): ID del usuario a validar.
            rol_requerido (str): Rol que se desea comprobar.

        Returns:
            bool: True si el usuario tiene el rol requerido, False en caso contrario.
        """
        return self.obtener_usuario(id_usuario).rol == rol_requerido
