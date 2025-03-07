class NoHayProductosError(Exception):
    """se lanza si se intenta mostrar el inventario pero no hay productos agregados"""
    pass