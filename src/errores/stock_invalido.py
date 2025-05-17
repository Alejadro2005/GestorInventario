class StockInvalidoError(Exception):
    """
    Excepción lanzada cuando se intenta establecer un stock no válido para un producto.
    
    Esta excepción se utiliza para indicar que se intentó asignar un valor
    de stock que no cumple con los criterios establecidos (por ejemplo,
    stock negativo o cero).
    """
    pass