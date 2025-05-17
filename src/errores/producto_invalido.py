class ProductoInvalidoError(Exception):
    """
    Excepción lanzada cuando se intenta crear o modificar un producto con datos inválidos.
    
    Esta excepción se utiliza para indicar que los datos del producto no cumplen
    con los criterios de validación establecidos (nombre vacío, precio negativo,
    stock negativo, etc.).
    
    Attributes:
        mensaje (str): Descripción detallada del error.
    """
    def __init__(self, mensaje="Los datos del producto no son válidos"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
