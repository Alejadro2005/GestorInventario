from datetime import datetime
from src.errores.nombre_usuario_invalido import NombreUsuarioInvalidoError
from src.errores.rol_invalido import RolInvalidoError
from src.errores.contrasena_invalida import ContraseñaInvalidaError
from src.errores.credenciales_invalidas import CredencialesInvalidasError
from src.errores.contrasena_expirada import ContraseñaExpiradaError

class Usuario:
    """
    Representa a un usuario dentro del sistema, incluyendo validaciones de rol, nombre y contraseña.

    Attributes:
        ROLES_VALIDOS (set): Conjunto de roles permitidos en el sistema.
        id (int): Identificador único del usuario.
        nombre (str): Nombre del usuario.
        rol (str): Rol asignado (admin, empleado, gerente).
        __contraseña (str): Contraseña privada del usuario.
        fecha_creacion (datetime): Fecha de creación de la cuenta.
    """

    ROLES_VALIDOS = {"admin", "empleado", "gerente"}

    def __init__(self, id: int, nombre: str, rol: str, contraseña: str):
        """
        Inicializa un objeto Usuario con las validaciones correspondientes.

        Args:
            id (int): Identificador único del usuario.
            nombre (str): Nombre del usuario (no vacío y hasta 50 caracteres).
            rol (str): Rol del usuario (debe ser uno de los ROLES_VALIDOS).
            contraseña (str): Contraseña del usuario (mínimo 4 caracteres).

        Raises:
            NombreUsuarioInvalidoError: Si el nombre es inválido.
            RolInvalidoError: Si el rol no es válido o tiene caracteres no permitidos.
            ContraseñaInvalidaError: Si la contraseña no cumple con los requisitos.
        """
        if not nombre or nombre.strip() == "":
            raise NombreUsuarioInvalidoError("El nombre de usuario no puede estar vacío")

        if len(nombre) > 50:
            raise NombreUsuarioInvalidoError("El nombre de usuario no puede tener más de 50 caracteres")

        if any(c for c in rol if not c.isalnum() and c not in {"_", "-"}):
            raise RolInvalidoError(f"El rol '{rol}' contiene caracteres inválidos")

        if rol not in self.ROLES_VALIDOS:
            raise RolInvalidoError(f"El rol '{rol}' no es válido")

        if not self.validar_contraseña(contraseña):
            raise ContraseñaInvalidaError("La contraseña no cumple con los requisitos mínimos")

        self.id = id
        self.nombre = nombre
        self.rol = rol
        self.__contraseña = contraseña
        self.fecha_creacion = datetime.now()

    def iniciar_sesion(self, contraseña: str) -> bool:
        """
        Verifica si la contraseña ingresada es correcta.

        Args:
            contraseña (str): Contraseña ingresada por el usuario.

        Returns:
            bool: True si la contraseña es correcta.

        Raises:
            CredencialesInvalidasError: Si la contraseña no coincide.
        """
        if self.__contraseña != contraseña:
            raise CredencialesInvalidasError("Credenciales incorrectas")
        return True

    def cambiar_contraseña(self, nueva_contraseña: str) -> str:
        """
        Cambia la contraseña del usuario si es válida.

        Args:
            nueva_contraseña (str): Nueva contraseña a establecer.

        Returns:
            str: La nueva contraseña establecida.

        Raises:
            ContraseñaInvalidaError: Si la nueva contraseña no es válida.
        """
        if not self.validar_contraseña(nueva_contraseña):
            raise ContraseñaInvalidaError("La contraseña no cumple con los requisitos mínimos")

        self.__contraseña = nueva_contraseña
        return self.__contraseña

    def validar_expiracion(self, fecha: str):
        """
        Verifica si la contraseña ha expirado (más de 365 días desde la fecha proporcionada).

        Args:
            fecha (str): Fecha en formato "DD/MM/AAAA".

        Raises:
            ValueError: Si el formato de la fecha es inválido.
            ContraseñaExpiradaError: Si han pasado más de 365 días desde la fecha ingresada.
        """
        try:
            fecha_ingresada = datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Formato de fecha inválido, debe ser DD/MM/AAAA")

        dias_transcurridos = (datetime.now() - fecha_ingresada).days
        if dias_transcurridos > 365:
            raise ContraseñaExpiradaError("La contraseña ha expirado")

    def to_dict(self) -> dict:
        """
        Convierte el objeto Usuario a un diccionario serializable.

        Returns:
            dict: Diccionario con los datos del usuario.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "rol": self.rol,
            "contraseña": self._Usuario__contraseña,
            "fecha_creacion": self.fecha_creacion.isoformat()
        }

    @staticmethod
    def validar_contraseña(contraseña: str) -> bool:
        """
        Verifica si la contraseña cumple con los requisitos mínimos.

        Args:
            contraseña (str): Contraseña a validar.

        Returns:
            bool: True si la contraseña tiene al menos 4 caracteres.
        """
        return len(contraseña) >= 4
