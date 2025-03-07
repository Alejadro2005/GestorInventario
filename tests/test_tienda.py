#test_tienda
import pytest
from src.modelos.venta import Venta
from src.modulos.tienda import Tienda
from src.modelos.inventario import Inventario
from src.modelos.producto import Producto
from src.errores.producto_invalido import ProductoInvalidoError
from src.errores.fecha_invalida import FechaInvalidaError
from src.errores.productos_duplicados import ProductoDuplicadoError
from src.errores.stock_insuficiente import StockInsuficienteError
from src.errores.venta_invalida import VentaInvalidaError
from src.errores.venta_producto_no_registrado import VentaProductoNoRegistradoError
from src.errores.descuento_invalido import DescuentoInvalidoError
from src.errores.total_invalido import TotalInvalidoError
from src.errores.venta_sin_empleado import VentaSinEmpleadoError
from src.errores.categoria_invalida import CategoriaInvalidaError
def test_registrar_venta1():
    producto1=Producto(1,"lapiz",500,1,"escolares",10)
    producto2=Producto(2,"cuaderno",1500,2,"escolares",10)
    gestor_inventario=Inventario()
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)
    productos_vendidos=[producto1,producto2]
    venta=Venta(1,"04/03/25",productos_vendidos,3500,1)
    gestor_ventas=Tienda()
    gestor_ventas.registrar_venta(venta)
    assert len(gestor_ventas.historial_ventas)==1


def test_validar_stock_venta_unica():
    producto1=Producto(1,"lapiz",500,10,"escolares",1)
    gestor_inventario=Inventario()
    gestor_inventario.agregar_producto(producto1)
    venta1=Venta(1,"04/03/25",producto1,2,1)
    gestor_ventas=Tienda()
    gestor_ventas.registrar_venta(venta1)
    assert gestor_ventas.validar_stock_venta(1,8)==True and gestor_ventas.validar_stock_venta(2,17)==True


def test_registrar_venta2():
    producto1=Producto(1,"lapiz",500,10,"escolares",1)
    producto2=Producto(2,"cuaderno",1500,20,"escolares",1)
    producto3=Producto(3,"corrector",1000,30,"escolares",1)
    gestor_inventario=Inventario()
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)
    gestor_inventario.agregar_producto(producto3)
    venta1=Venta(1,"04/03/25",producto1,500,1)
    venta2=Venta(2,"05/03/25",producto2,3000,1)
    venta3=Venta(2,"05/03/25",producto3,3000,2)
    gestor_ventas=Tienda()
    gestor_ventas.registrar_venta(venta1)
    gestor_ventas.registrar_venta(venta2)
    gestor_ventas.registrar_venta(venta3)
    assert len(gestor_ventas.historial_ventas)==3
    

def test_calcular_total():
    producto=Producto(34,"lapiz",500,10,"escolar",1)
    gestor_inventario=Inventario()
    gestor_inventario.agregar_producto(producto)
    venta=Venta(1,"03/03/25",producto,1,1)
    assert venta.calcular_total(producto,2)==1000


def test_validar_stock_ventas():
    producto1=Producto(1,"lapiz",500,10,"escolares",1)
    producto2=Producto(2,"cuaderno",1500,20,"escolares",1)
    producto3=Producto(3,"corrector",1000,30,"escolares",1)
    gestor_inventario=Inventario()
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)
    gestor_inventario.agregar_producto(producto3)
    venta1=Venta(1,"03/05/25",producto1,2,1)
    venta2=Venta(1,"03/05/25",producto2,6,1)
    venta3=Venta(1,"03/05/25",producto3,1,1)
    assert (venta1.validar_stock(producto1)==9 and venta2.validar_stock(producto2)==14 and venta3.validar_stock(producto3)==29)


def test_generar_historial():
    producto=Producto(1,"lapiz",500,10,"escolar",1)
    gestor_inventario=Inventario()
    gestor_inventario.agregar_producto(producto)
    venta=Venta(1,"03/04/25",producto,2,1)
    gestor_venta=Tienda()
    gestor_venta.registrar_venta(venta)
    assert gestor_venta.generar_historial()==venta

#tests error
def test_producto_precio_negativo():
    with pytest.raises(ProductoInvalidoError, match="El precio debe ser mayor a cero"):
        Producto(1, "lapiz", -100, 10, "escolares", 1)


def test_producto_stock_negativo():
    with pytest.raises(ProductoInvalidoError, match="El stock no puede ser negativo"):
        Producto(2, "cuaderno", 1500, -5, "escolares", 1)


def test_producto_duplicado():
    producto = Producto(1, "lapiz", 500, 10, "escolares", 1)
    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto)

    with pytest.raises(ProductoDuplicadoError, match="Producto con ID 1 ya existe en el inventario"):
        gestor_inventario.agregar_producto(producto)


def test_stock_insuficiente():
    producto = Producto(1, "lapiz", 500, 1, "escolares", 1)
    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto)

    venta = Venta(1, "04/03/25", producto, 2, 1)  

    gestor_ventas = Tienda()

    with pytest.raises(StockInsuficienteError, match="Stock insuficiente para el producto lapiz"):
        gestor_ventas.registrar_venta(venta)


def test_venta_cantidad_negativa():
    producto = Producto(1, "lapiz", 500, 10, "escolares", 1)
    with pytest.raises(VentaInvalidaError, match="La cantidad debe ser mayor a cero"):
        Venta(1, "04/03/25", producto, -5, 1)


def test_fecha_invalida():
    producto = Producto(1, "lapiz", 500, 10, "escolares", 1)
    with pytest.raises(FechaInvalidaError, match="La fecha 32/13/25 es inválida"):
        Venta(1, "32/13/25", producto, 2, 1) 


#test caso extremo
def test_venta_producto_fantasma():
    producto = Producto(99, "No existe", 100, 1, "Fantasma", 1)
    with pytest.raises(VentaProductoNoRegistradoError):
        Venta(7, "04/03/25", producto, 1, 1)

def test_descuento_excesivo():
    producto=Producto(1,"lapiz",10,1,"escolar",1)
    productos_vendidos=[producto]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, 100)

    with pytest.raises(DescuentoInvalidoError):
        venta.aplicar_descuento(150)  # 150% de descuento

def test_venta_sin_productos():
    productos_vendidos=[]
    with pytest.raises(VentaInvalidaError):
        Venta(9, "04/03/25", productos_vendidos, 0, 1)

def test_venta_con_total_negativo():
    producto = Producto(5, "Teclado", 50, 1, "Electrónica", 1)
    productos_vendidos=[producto]
    with pytest.raises(TotalInvalidoError):
        Venta(14, "04/03/25", productos_vendidos, -50, 1)

def test_venta_sin_empleado():

    producto = Producto(6, "Mouse", 30, 1, "Electrónica", 1)
    productos_vendidos=[producto]
    with pytest.raises(VentaSinEmpleadoError):
        Venta(15,"04/03/25", productos_vendidos, 30, None)

def test_venta_producto_categoria_invalida():
    producto = Producto(8, "Cámara", 500, 1, "Categoría Fantasma", 1)  # Categoría inexistente
    productos_vendidos=[producto]
    with pytest.raises(CategoriaInvalidaError):
        Venta(17,"04/03/25", productos_vendidos,500,1)
