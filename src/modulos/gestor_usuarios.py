from src.modelos.usuario import Usuario
from src.errores.usuario_no_encontrado import UsuarioNoEncontradoError
from src.errores.usuario_duplicado import UsuarioDuplicadoError
from .persistencia import PersistenciaJSON

RUTA_USUARIOS = "data/usuarios.json"


class GestorUsuarios:
    def __init__(self):
        """Carga los usuarios desde el archivo JSON al iniciar."""
        self.usuarios = {}
        datos = PersistenciaJSON.cargar_datos(RUTA_USUARIOS)
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
        """Crea un nuevo usuario y lo guarda en el archivo JSON."""
        if usuario.id in self.usuarios:
            raise UsuarioDuplicadoError(f"El usuario con ID {usuario.id} ya existe.")
        self.usuarios[usuario.id] = usuario
        self.guardar_usuarios()
        return f"Usuario '{usuario.nombre}' creado con éxito."

    def guardar_usuarios(self):
        """Guarda usando el formato correcto de claves."""
        datos = [u.to_dict() for u in self.usuarios.values()]
        PersistenciaJSON.guardar_datos(RUTA_USUARIOS, datos)

    def eliminar_usuario(self, id_usuario: int):
        """Elimina un usuario si existe y guarda los cambios."""
        if id_usuario not in self.usuarios:
            raise UsuarioNoEncontradoError(f"El usuario con ID {id_usuario} no existe.")
        nombre = self.usuarios[id_usuario].nombre
        del self.usuarios[id_usuario]
        self.guardar_usuarios()
        return f"Usuario '{nombre}' eliminado con éxito."

    def obtener_usuario(self, id_usuario: int) -> Usuario:
        """Obtiene un usuario por ID."""
        if id_usuario not in self.usuarios:
            raise UsuarioNoEncontradoError(f"El usuario con ID {id_usuario} no existe.")
        return self.usuarios[id_usuario]

    def validar_rol(self, id_usuario: int, rol_requerido: str) -> bool:
        """Verifica si un usuario tiene el rol requerido."""
        return self.obtener_usuario(id_usuario).rol == rol_requerido