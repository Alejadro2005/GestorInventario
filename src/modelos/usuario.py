from src.errores.contrasena_invalida import ContraseñaInvalidaError
from src.errores.credenciales_invalidas import CredencialesInvalidasError
from datetime import datetime
from src.errores.nombre_usuario_invalido import NombreUsuarioInvalidoError
from src.errores.rol_invalido import RolInvalidoError
from src.errores.contrasena_expirada import ContraseñaExpiradaError


class Usuario:
    ROLES_VALIDOS = {"admin", "empleado", "gerente"}  # Lista de roles permitidos

    def __init__(self, id: int, nombre: str, rol: str, contraseña: str):
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
        self.__contraseña = contraseña  # Almacena la contraseña de forma privada
        self.fecha_creacion = datetime.now()  # Guarda la fecha de creación de la cuenta

    def iniciar_sesion(self, contraseña: str) -> bool:
        if self.__contraseña != contraseña:
            raise CredencialesInvalidasError("Credenciales incorrectas")
        return True

    def cambiar_contraseña(self, nueva_contraseña: str):
        if not self.validar_contraseña(nueva_contraseña):
            raise ContraseñaInvalidaError("La contraseña no cumple con los requisitos mínimos")

        self.__contraseña = nueva_contraseña
        return self.__contraseña

    def validar_expiracion(self, fecha: str):
        """Verifica si la contraseña ha expirado. Se asume que caduca después de 365 días."""
        try:
            fecha_ingresada = datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Formato de fecha inválido, debe ser DD/MM/AAAA")

        dias_transcurridos = (datetime.now() - fecha_ingresada).days
        if dias_transcurridos > 365:
            raise ContraseñaExpiradaError("La contraseña ha expirado")

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "rol": self.rol,
            "contraseña": self._Usuario__contraseña,  # Cambiar clave a "contraseña"
            "fecha_creacion": self.fecha_creacion.isoformat()
        }

    @staticmethod
    def validar_contraseña(contraseña: str) -> bool:
        """Valida si la contraseña tiene al menos 4 caracteres."""
        return len(contraseña) >= 4