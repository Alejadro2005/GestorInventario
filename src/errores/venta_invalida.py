class VentaInvalidaError(Exception):
    """
    Excepción lanzada cuando se intenta realizar una venta con datos inválidos.
    
    Esta excepción se utiliza para indicar que los datos de la venta no cumplen
    con los criterios establecidos (por ejemplo, lista de productos vacía,
    total inválido, etc.).
    """
    pass
