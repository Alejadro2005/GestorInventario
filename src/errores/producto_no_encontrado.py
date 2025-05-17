class ProductoNoEncontradoError(Exception):
    """
    Excepción lanzada cuando se intenta acceder a un producto que no existe en el sistema.
    
    Esta excepción se utiliza para indicar que se intentó realizar una operación
    sobre un producto que no está registrado en el inventario.
    """
    pass