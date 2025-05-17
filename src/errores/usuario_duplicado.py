class UsuarioDuplicadoError(Exception):
    """
    Excepción lanzada cuando se intenta registrar un usuario que ya existe en el sistema.
    
    Esta excepción se utiliza para indicar que se intentó crear un usuario
    con un nombre o identificador que ya está registrado en el sistema.
    """
    pass