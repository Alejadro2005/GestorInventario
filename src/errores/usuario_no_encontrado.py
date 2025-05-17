class UsuarioNoEncontradoError(Exception):
    """
    Excepción lanzada cuando se intenta acceder a un usuario que no existe en el sistema.
    
    Esta excepción se utiliza para indicar que se intentó realizar una operación
    sobre un usuario que no está registrado en el sistema.
    """
    pass