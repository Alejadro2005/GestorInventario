class RolInvalidoError(Exception):
    """
    Excepción lanzada cuando se asigna un rol no válido a un usuario.
    
    Esta excepción se utiliza para indicar que se intentó asignar un rol
    que no está permitido en el sistema (por ejemplo, roles que no son 'admin' o 'empleado').
    
    Attributes:
        mensaje (str): Descripción detallada del error.
    """
    def __init__(self, mensaje="El rol asignado no es válido"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)