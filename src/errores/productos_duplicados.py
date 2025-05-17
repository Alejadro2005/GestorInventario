class ProductoDuplicadoError(Exception):
    """
    Excepción lanzada cuando se intenta agregar un producto que ya existe en el sistema.
    
    Esta excepción se utiliza para indicar que se intentó registrar un producto
    con un nombre o identificador que ya está registrado en el inventario.
    """
    pass