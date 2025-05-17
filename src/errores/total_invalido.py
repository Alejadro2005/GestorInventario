class TotalInvalidoError(Exception):
    """
    Excepción lanzada cuando se intenta establecer un total no válido para una venta.
    
    Esta excepción se utiliza para indicar que el total calculado para una venta
    no cumple con los criterios establecidos (por ejemplo, total negativo o cero).
    """
    pass