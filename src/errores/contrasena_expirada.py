class ContrasenaExpiradaError(Exception):
    """
    Excepción lanzada cuando una contraseña ha expirado.
    
    Esta excepción se utiliza para indicar que la contraseña de un usuario
    ha superado su período de validez y necesita ser actualizada.
    """
    pass