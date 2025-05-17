class DescuentoInvalidoError(Exception):
    """
    Excepción lanzada cuando se intenta aplicar un descuento no válido.
    
    Esta excepción se utiliza para indicar que el descuento proporcionado
    no cumple con los criterios establecidos (por ejemplo, porcentaje negativo
    o mayor al 100%).
    
    Attributes:
        mensaje (str): Descripción detallada del error.
    """
    def __init__(self, mensaje="El descuento debe estar entre 0 y 100"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)
