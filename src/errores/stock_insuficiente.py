class StockInsuficienteError(Exception):
    """
    Excepción lanzada cuando se intenta realizar una operación que requiere
    más stock del disponible.
    
    Esta excepción se utiliza para indicar que se intentó realizar una venta
    o modificar el stock de un producto con una cantidad mayor a la disponible.
    """
    pass