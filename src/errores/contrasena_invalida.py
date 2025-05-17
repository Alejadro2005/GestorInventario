class ContrasenaInvalidaError(Exception):
    """
    Excepción lanzada cuando una contraseña no cumple con los requisitos de validación.
    
    Esta excepción se utiliza para indicar que la contraseña proporcionada
    no cumple con los criterios de seguridad establecidos (longitud mínima,
    caracteres especiales, etc.).
    """
    pass