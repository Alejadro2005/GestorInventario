class PrecioInvalidoError(Exception):
    """
    Se lanza cuando el precio de un producto es negativo, cero o no cumple con los criterios válidos.
    """
    pass