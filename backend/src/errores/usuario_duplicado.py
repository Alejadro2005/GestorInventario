class UsuarioDuplicadoError(Exception):
    """Se lanza cuando se intenta crear un usuario con un ID que ya existe en el sistema."""
    pass