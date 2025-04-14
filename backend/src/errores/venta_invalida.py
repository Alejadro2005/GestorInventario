class VentaInvalidaError(Exception):
    """Se lanza cuando la venta no cumple las reglas de negocio (cantidad <= 0, etc)."""
    pass
