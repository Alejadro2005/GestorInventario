class VentaProductoCategoriaInvalidaError(Exception):
    """
    Excepción lanzada cuando se intenta vender un producto de una categoría no permitida.
    
    Esta excepción se utiliza para indicar que se intentó realizar una venta
    con un producto cuya categoría no está permitida para la venta.
    """
    pass