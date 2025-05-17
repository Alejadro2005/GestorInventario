class CredencialesInvalidasError(Exception):
    """
    Excepción lanzada cuando las credenciales de inicio de sesión son inválidas.
    
    Esta excepción se utiliza para indicar que el usuario o contraseña
    proporcionados no son correctos o no coinciden con los registros del sistema.
    """
    pass