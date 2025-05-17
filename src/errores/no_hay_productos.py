class NoHayProductosError(Exception):
    """
    Excepción lanzada cuando se intenta realizar una operación que requiere productos
    pero no hay ninguno disponible en el sistema.
    
    Esta excepción se utiliza para indicar que se intentó acceder a una lista
    de productos que está vacía o no hay productos que cumplan con ciertos criterios.
    """
    pass