from src.modelos.venta import Venta
class Tienda():
    def __init__(self,historial_ventas=[]):
        self.historial_ventas=historial_ventas
    def registrar_venta(self,venta:Venta):
        pass
    def generar_historial(self)->list[Venta]:
        pass
    def validar_stock_venta(self,id_producto:int,cantidad:int)->bool:
        pass