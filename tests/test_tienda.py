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
from src.errores.precio_invalido import PrecioInvalidoError
from src.errores.stock_insuficiente import StockInsuficienteError


def test_registrar_venta1():
    producto1 = Producto(1, "lapiz", 500, 1, "escolar", 10)
    producto2 = Producto(2, "cuaderno", 1500, 2, "escolar", 10)
    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)
    productos_vendidos = [(producto1, 1), (producto2, 2)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, gestor_inventario)
    gestor_ventas = Tienda()
    ventas_actualizadas = gestor_ventas.registrar_venta(venta, gestor_inventario)
    assert len(ventas_actualizadas) == 1


def test_registrar_venta3():
    producto1 = Producto(1, "lapiz", 500, 10, "escolar", 10)
    producto2 = Producto(2, "cuaderno", 1500, 20, "escolar", 10)

    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)

    productos_vendidos = [(producto1, 2), (producto2, 1)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, gestor_inventario)

    gestor_ventas = Tienda()
    gestor_ventas.registrar_venta(venta, gestor_inventario)

    assert len(gestor_ventas.historial_ventas) == 1


def test_registrar_venta2():
    producto1 = Producto(1, "lapiz", 500, 10, "escolar", 1)
    producto2 = Producto(2, "cuaderno", 1500, 20, "escolar", 1)
    producto3 = Producto(3, "corrector", 1000, 30, "escolar", 1)
    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)
    gestor_inventario.agregar_producto(producto3)
    productos_venta1 = [(producto1, 2)]
    productos_venta2 = [(producto2, 2)]
    productos_venta3 = [(producto3, 2)]
    venta1 = Venta(1, "04/03/25", productos_venta1, 1, gestor_inventario)
    venta2 = Venta(2, "05/03/25", productos_venta2, 1, gestor_inventario)
    venta3 = Venta(3, "05/03/25", productos_venta3, 2, gestor_inventario)
    gestor_ventas = Tienda()
    gestor_ventas.registrar_venta(venta1, gestor_inventario)
    gestor_ventas.registrar_venta(venta2, gestor_inventario)
    gestor_ventas.registrar_venta(venta3, gestor_inventario)
    assert len(gestor_ventas.historial_ventas) == 3


def test_calcular_total():
    producto = Producto(34, "lapiz", 500, 10, "escolar", 1)
    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto)

    producto_vendido = [(producto, 2)]  # Producto con cantidad
    venta = Venta(1, "03/03/25", producto_vendido, 1, gestor_inventario)

    assert venta.calcular_total() == 1000  # 500 * 2


def test_validar_stock_ventas():
    producto1 = Producto(1, "lapiz", 500, 10, "escolar", 1)
    producto2 = Producto(2, "cuaderno", 1500, 20, "escolar", 1)
    producto3 = Producto(3, "corrector", 1000, 30, "escolar", 1)
    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)
    gestor_inventario.agregar_producto(producto3)
    productos_venta1 = [(producto1, 1)]
    productos_venta2 = [(producto2, 6)]
    productos_venta3 = [(producto3, 1)]
    venta1 = Venta(1, "03/05/25", productos_venta1, 1, gestor_inventario)
    venta2 = Venta(2, "03/05/25", productos_venta2, 1, gestor_inventario)
    venta3 = Venta(3, "03/05/25", productos_venta3, 1, gestor_inventario)
    tienda = Tienda()
    assert tienda.validar_stock_venta(1, venta1.productos_vendidos[0][1], gestor_inventario) == True and \
           tienda.validar_stock_venta(2, venta2.productos_vendidos[0][1], gestor_inventario) == True and \
           tienda.validar_stock_venta(3, venta3.productos_vendidos[0][1], gestor_inventario) == True

    # assert (venta1.validar_stock(producto1)==9 and venta2.validar_stock(producto2)==14 and venta3.validar_stock(producto3)==29)


def test_generar_historial():
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto)
    producto_vendido = [(producto, 2)]
    venta = Venta(1, "03/04/25", producto_vendido, 1, gestor_inventario)
    gestor_venta = Tienda()
    gestor_venta.registrar_venta(venta, gestor_inventario)
    assert gestor_venta.generar_historial() == [venta]  # Se compara con una lista que contiene el objeto


# tests error
def test_producto_precio_negativo():
    with pytest.raises(PrecioInvalidoError, match="El precio del producto debe ser mayor a cero."):
        Producto(1, "lapiz", -100, 10, "escolares", 1)


def test_producto_stock_negativo():
    with pytest.raises(ProductoInvalidoError, match="La cantidad del producto no puede ser negativa."):
        Producto(2, "cuaderno", 1500, -5, "escolares", 1)


def test_producto_duplicado():
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto)

    with pytest.raises(ProductoDuplicadoError, match="El producto con ID 1 ya existe en el inventario"):
        gestor_inventario.agregar_producto(producto)


def test_stock_insuficiente():
    producto = Producto(1, "lapiz", 500, 1, "escolar", 1)
    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto)
    productos_vendidos = [(producto, 2)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, gestor_inventario)

    gestor_ventas = Tienda()

    with pytest.raises(StockInsuficienteError, match="Stock insuficiente para el producto lapiz"):
        gestor_ventas.registrar_venta(venta, gestor_inventario)


def test_venta_cantidad_negativa():
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    productos_vendidos = [(producto, -5)]
    inventario = Inventario()
    inventario.agregar_producto(producto)
    with pytest.raises(VentaInvalidaError, match="La cantidad debe ser mayor a cero"):
        venta = Venta(1, "04/03/25", productos_vendidos, 1, inventario)


def test_fecha_invalida():
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    productos_vendidos = [(producto, 2)]
    inventario = Inventario()
    with pytest.raises(FechaInvalidaError, match="La fecha 32/13/25 es inválida"):
        Venta(1, "32/13/25", productos_vendidos, 1, inventario)

    # test caso extremo


def test_venta_producto_fantasma():
    producto = Producto(99, "No existe", 100, 1, "Fantasma", 1)
    productos_vendidos = [(producto, 1)]
    inventario = Inventario()
    with pytest.raises(VentaProductoNoRegistradoError):
        Venta(7, "04/03/25", productos_vendidos, 1, inventario)


def test_descuento_excesivo():
    producto = Producto(1, "lapiz", 10, 1, "escolar", 1)
    productos_vendidos = [(producto, 2)]
    inventario = Inventario()
    inventario.agregar_producto(producto)
    venta = Venta(1, "04/03/25", productos_vendidos, 100, inventario)

    with pytest.raises(DescuentoInvalidoError):
        venta.aplicar_descuento(150)  # 150% de descuento


def test_venta_sin_productos():
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    productos_vendidos = []
    inventario = Inventario()
    inventario.agregar_producto(producto)
    with pytest.raises(VentaInvalidaError):
        Venta(9, "04/03/25", productos_vendidos, 1, inventario)


def test_registrar_venta_stock_insuficiente2():
    gestor_ventas = Tienda()
    gestor_inventario = Inventario()

    producto = Producto(1, "lapiz", 500, 1, "escolar", 5)  # Solo hay 5 en stock
    gestor_inventario.agregar_producto(producto)

    productos_vendidos = [(producto, 10)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, gestor_inventario)
    with pytest.raises(StockInsuficienteError, match="Stock insuficiente para el producto lapiz"):
        gestor_ventas.registrar_venta(venta, gestor_inventario)


def test_venta_sin_empleado():
    producto = Producto(6, "Mouse", 30, 1, "Electrónica", 1)
    productos_vendidos = [(producto, 30)]
    inventario = Inventario()
    inventario.agregar_producto(producto)
    with pytest.raises(VentaSinEmpleadoError):
        Venta(15, "04/03/25", productos_vendidos, None, inventario)


def test_venta_producto_categoria_invalida():
    producto = Producto(8, "Cámara", 500, 1, "Categoría Fantasma", 1)  # Categoría inexistente
    productos_vendidos = [(producto, 500)]
    invetario = Inventario()
    invetario.agregar_producto(producto)
    with pytest.raises(CategoriaInvalidaError):
        Venta(17, "04/03/25", productos_vendidos, 1, invetario)
