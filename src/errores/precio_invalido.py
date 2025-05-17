class PrecioInvalidoError(Exception):
    """
    Excepción lanzada cuando un precio no cumple con los criterios de validación.
    
    Esta excepción se utiliza para indicar que el precio de un producto
    no es válido (por ejemplo, es negativo o cero).
    
    Attributes:
        mensaje (str): Descripción detallada del error.
    """
    def __init__(self, mensaje="El precio debe ser mayor que cero"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)