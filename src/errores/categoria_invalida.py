class CategoriaInvalidaError(Exception):
    """
    Excepción lanzada cuando se asigna una categoría no válida a un producto.
    
    Esta excepción se utiliza para indicar que la categoría proporcionada
    no cumple con los criterios establecidos (por ejemplo, categoría vacía
    o no permitida en el sistema).
    
    Attributes:
        mensaje (str): Descripción detallada del error.
    """
    def __init__(self, mensaje="La categoría proporcionada no es válida"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)