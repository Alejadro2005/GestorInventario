class NombreUsuarioInvalidoError(Exception):
    """
    Excepción lanzada cuando el nombre de usuario no cumple con los criterios de validación.
    
    Esta excepción se utiliza para indicar que el nombre de usuario proporcionado
    no cumple con los requisitos establecidos (longitud mínima, caracteres permitidos, etc.).
    
    Attributes:
        mensaje (str): Descripción detallada del error.
    """
    def __init__(self, mensaje="El nombre de usuario no cumple con los requisitos"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)