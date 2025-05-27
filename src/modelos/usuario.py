from datetime import datetime
from errores.nombre_usuario_invalido import NombreUsuarioInvalidoError
from errores.rol_invalido import RolInvalidoError
from errores.contrasena_invalida import ContrasenaInvalidaError
from errores.credenciales_invalidas import CredencialesInvalidasError
from errores.contrasena_expirada import ContrasenaExpiradaError

class Usuario:
    """
    Clase que representa un usuario del sistema.
    
    Esta clase maneja la lógica de negocio relacionada con los usuarios,
    incluyendo validaciones de roles y credenciales.

    Attributes:
        ROLES_VALIDOS (list): Lista de roles permitidos en el sistema
        id (int): Identificador único del usuario
        nombre (str): Nombre del usuario
        rol (str): Rol del usuario en el sistema
        password (str): Contraseña encriptada del usuario
    """

    ROLES_VALIDOS = ['admin', 'vendedor', 'inventarista']

    def __init__(self, id, nombre, rol, password):
        """
        Inicializa un nuevo usuario.

        Args:
            id (int): Identificador único del usuario
            nombre (str): Nombre del usuario
            rol (str): Rol del usuario en el sistema
            password (str): Contraseña encriptada del usuario
        """
        self.id = id
        self.nombre = nombre
        self.rol = rol
        self.password = password

    def validar(self):
        """
        Valida que el usuario cumpla con todas las reglas de negocio.
        
        Raises:
            ValueError: Si alguna validación falla
        """
        if not self.nombre or len(self.nombre) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        if self.rol not in self.ROLES_VALIDOS:
            raise ValueError(f"El rol debe ser uno de: {', '.join(self.ROLES_VALIDOS)}")
        if not self.password:
            raise ContrasenaInvalidaError("La contraseña es requerida")

    def to_dict(self):
        """
        Convierte el usuario a un diccionario.
        
        Returns:
            dict: Diccionario con los datos del usuario
        """
        return {
            'id': self.id,
            'nombre': self.nombre,
            'rol': self.rol,
            'password': self.password
        }

    @classmethod
    def from_dict(cls, data):
        """
        Crea un usuario a partir de un diccionario.
        
        Args:
            data (dict): Diccionario con los datos del usuario
            
        Returns:
            Usuario: Nueva instancia de Usuario
        """
        return cls(
            id=data['id'],
            nombre=data['nombre'],
            rol=data['rol'],
            password=data['password']
        )

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
        if self.password != contraseña:
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
            raise ContrasenaInvalidaError("La contraseña no cumple con los requisitos mínimos")

        self.password = nueva_contraseña
        return self.password

    def validar_expiracion(self, fecha: str):
        """
        Verifica si la contraseña ha expirado (más de 365 días desde la fecha proporcionada).

        Args:
            fecha (str): Fecha en formato "DD/MM/AAAA".

        Raises:
            ValueError: Si el formato de la fecha es inválido.
            ContrasenaExpiradaError: Si han pasado más de 365 días desde la fecha ingresada.
        """
        try:
            fecha_ingresada = datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            raise ValueError("Formato de fecha inválido, debe ser DD/MM/AAAA")

        dias_transcurridos = (datetime.now() - fecha_ingresada).days
        if dias_transcurridos > 365:
            raise ContrasenaExpiradaError("La contraseña ha expirado")

    @staticmethod
    def validar_contraseña(contraseña: str) -> bool:
        """
        Verifica si la contraseña cumple con los requisitos mínimos.

        Args:
            contraseña (str): Contraseña a validar.

        Returns:
            bool: True si la contraseña tiene al menos 4 caracteres y no está vacía.
        """
        return len(contraseña) >= 4 and contraseña.strip() != ""
