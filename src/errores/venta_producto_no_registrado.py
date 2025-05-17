class VentaProductoNoRegistradoError(Exception):
    """
    Excepción lanzada cuando se intenta vender un producto que no está registrado en el sistema.
    
    Esta excepción se utiliza para indicar que se intentó realizar una venta
    con un producto que no existe en el inventario.
    
    Attributes:
        mensaje (str): Descripción detallada del error.
    """
    def __init__(self, mensaje="El producto no está registrado en el sistema"):
        self.mensaje = mensaje
        super().__init__(self.mensaje)