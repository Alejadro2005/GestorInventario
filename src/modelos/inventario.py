from src.modelos.producto import Producto
class Inventario():
    def __init__(self,productos:list[Producto]=[]):
        self.productos=productos
    def agregar_producto(self,producto:Producto):
        pass
    def eliminar_producto(self,id_producto:int):
        pass
    def filtrar_por_stock_bajo(self)->list[Producto]:
        pass
    def actualizar_stock(self,id_producto:int,cantidad):
        pass
