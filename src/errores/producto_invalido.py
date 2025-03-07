class ProductoInvalidoError(Exception):
    """
    Se lanza cuando se intenta agregar o manipular un producto que tiene datos inválidos.
    Ejemplos: nombre vacío, precio negativo, categoría inválida, etc.
    """
    pass
