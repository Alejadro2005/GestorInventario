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
from src.database.sqlite_database import SQLiteDatabase


def test_registrar_venta1(inventario_limpio):
    """
    Test para verificar que se pueda registrar una venta con múltiples productos 
    y que se agregue correctamente al historial de ventas.

    Se crean dos productos, se agregan al inventario, se registra una venta y 
    se verifica que el historial de ventas contenga un registro.

    Raises:
        AssertionError: Si el historial de ventas no contiene el registro esperado.
    """
    producto1 = Producto(1, "lapiz", 500, 1, "escolar", 10)
    producto2 = Producto(2, "cuaderno", 1500, 2, "escolar", 10)
    gestor_inventario = inventario_limpio
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)
    productos_vendidos = [(producto1.to_dict(), 1), (producto2.to_dict(), 2)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, gestor_inventario)
    gestor_ventas = Tienda(gestor_inventario)
    gestor_ventas.registrar_venta(venta, gestor_inventario)
    assert len(gestor_ventas.generar_historial()) == 1

def test_registrar_venta3(inventario_limpio):
    producto1 = Producto(1, "lapiz", 500, 10, "escolar", 10)
    producto2 = Producto(2, "cuaderno", 1500, 20, "escolar", 10)
    gestor_inventario = inventario_limpio
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)
    productos_vendidos = [(producto1.to_dict(), 2), (producto2.to_dict(), 1)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, gestor_inventario)
    gestor_ventas = Tienda(gestor_inventario)
    gestor_ventas.registrar_venta(venta, gestor_inventario)
    assert len(gestor_ventas.generar_historial()) == 1


def test_registrar_venta2(inventario_limpio):
    """
    Test para registrar varias ventas y asegurarse de que se agreguen correctamente 
    al historial de ventas.

    Se crean tres productos diferentes, se registran tres ventas y se verifica 
    que el historial de ventas contenga tres registros.

    Raises:
        AssertionError: Si el historial de ventas no contiene tres registros.
    """
    producto1 = Producto(1, "lapiz", 500, 10, "escolar", 1)
    producto2 = Producto(2, "cuaderno", 1500, 20, "escolar", 1)
    producto3 = Producto(3, "corrector", 1000, 30, "escolar", 1)
    gestor_inventario = inventario_limpio
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)
    gestor_inventario.agregar_producto(producto3)
    productos_venta1 = [(producto1.to_dict(), 2)]
    productos_venta2 = [(producto2.to_dict(), 2)]
    productos_venta3 = [(producto3.to_dict(), 2)]
    venta1 = Venta(1, "04/03/25", productos_venta1, 1, gestor_inventario)
    venta2 = Venta(2, "05/03/25", productos_venta2, 1, gestor_inventario)
    venta3 = Venta(3, "05/03/25", productos_venta3, 2, gestor_inventario)
    gestor_ventas = Tienda(gestor_inventario)
    gestor_ventas.registrar_venta(venta1, gestor_inventario)
    gestor_ventas.registrar_venta(venta2, gestor_inventario)
    gestor_ventas.registrar_venta(venta3, gestor_inventario)
    assert len(gestor_ventas.generar_historial()) == 3


def test_calcular_total(inventario_limpio):
    """
    Test para verificar que el cálculo del total de una venta se realice correctamente.

    Se registra una venta con un solo producto y se verifica que el total calculado
    sea el correcto.

    Raises:
        AssertionError: Si el total calculado no es el esperado.
    """
    producto = Producto(34, "lapiz", 500, 10, "escolar", 1)
    gestor_inventario = inventario_limpio
    gestor_inventario.agregar_producto(producto)
    producto_vendido = [(producto.to_dict(), 2)]  # Producto con cantidad
    venta = Venta(1, "03/03/25", producto_vendido, 1, gestor_inventario)
    assert venta.calcular_total() == 1000  # 500 * 2


def test_validar_stock_ventas(inventario_limpio):
    """
    Test para verificar la validación de stock antes de realizar una venta.

    Se crea un inventario con tres productos y se verifica que el stock sea suficiente
    para realizar la venta. Si el stock es suficiente, se confirma que la venta se pueda realizar.

    Raises:
        AssertionError: Si la validación de stock no es correcta.
    """
    producto1 = Producto(1, "lapiz", 500, 10, "escolar", 1)
    producto2 = Producto(2, "cuaderno", 1500, 20, "escolar", 1)
    producto3 = Producto(3, "corrector", 1000, 30, "escolar", 1)
    gestor_inventario = inventario_limpio
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)
    gestor_inventario.agregar_producto(producto3)
    productos_venta1 = [(producto1.to_dict(), 1)]
    productos_venta2 = [(producto2.to_dict(), 6)]
    productos_venta3 = [(producto3.to_dict(), 1)]
    venta1 = Venta(1, "03/05/25", productos_venta1, 1, gestor_inventario)
    venta2 = Venta(2, "03/05/25", productos_venta2, 1, gestor_inventario)
    venta3 = Venta(3, "03/05/25", productos_venta3, 1, gestor_inventario)
    tienda = Tienda(gestor_inventario)
    assert tienda.validar_stock_venta(1, venta1.productos_vendidos[0][1], gestor_inventario) == True and \
           tienda.validar_stock_venta(2, venta2.productos_vendidos[0][1], gestor_inventario) == True and \
           tienda.validar_stock_venta(3, venta3.productos_vendidos[0][1], gestor_inventario) == True

def test_generar_historial(inventario_limpio):
    """
    Test para verificar que se genere el historial de ventas correctamente.

    Se registra una venta y luego se genera el historial de ventas, 
    verificando que la estructura sea la esperada.

    Raises:
        AssertionError: Si el historial generado no coincide con el esperado.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    gestor_inventario = inventario_limpio
    gestor_inventario.agregar_producto(producto)
    producto_vendido = [(producto.to_dict(), 2)]
    venta = Venta(1, "03/04/25", producto_vendido, 1, gestor_inventario)
    gestor_venta = Tienda(gestor_inventario)
    gestor_venta.registrar_venta(venta, gestor_inventario)

    historial = gestor_venta.generar_historial()
    assert len(historial) == 1
    assert historial[0]["id"] == 1
    assert historial[0]["productos"] == ["lapiz (x2)"]
    assert historial[0]["total"] == 1000
    assert historial[0]["empleado"] == 1

# tests error
def test_producto_precio_negativo():
    """
    Test para verificar que un producto con un precio negativo lance el error 
    `PrecioInvalidoError`.

    Se crea un producto con un precio negativo y se verifica que se lance el error adecuado
    con el mensaje esperado.

    Raises:
        PrecioInvalidoError: Si el precio del producto es negativo.
    """
    with pytest.raises(PrecioInvalidoError, match="El precio del producto debe ser mayor a cero."):
        Producto(1, "lapiz", -100, 10, "escolares", 1)


def test_producto_stock_negativo():
    """
    Test para verificar que un producto con stock negativo lance el error 
    `ProductoInvalidoError`.

    Se crea un producto con una cantidad negativa y se verifica que se lance el error adecuado
    con el mensaje esperado.

    Raises:
        ProductoInvalidoError: Si la cantidad del producto es negativa.
    """
    with pytest.raises(ProductoInvalidoError, match="La cantidad del producto no puede ser negativa."):
        Producto(2, "cuaderno", 1500, -5, "escolares", 1)


def test_producto_duplicado(inventario_limpio):
    """
    Test para verificar que si se intenta agregar un producto duplicado al inventario, 
    se lance el error `ProductoDuplicadoError`.

    Se agrega un producto al inventario y luego se intenta agregarlo de nuevo para verificar 
    que se lance el error con el mensaje correspondiente.

    Raises:
        ProductoDuplicadoError: Si el producto ya existe en el inventario.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    gestor_inventario = inventario_limpio
    gestor_inventario.agregar_producto(producto)

    with pytest.raises(ProductoDuplicadoError, match="El producto con ID 1 ya existe en el inventario"):
        gestor_inventario.agregar_producto(producto)


def test_stock_insuficiente():
    """
    Test para verificar que se lance el error `StockInsuficienteError` cuando el stock
    de un producto no es suficiente para satisfacer una venta.

    Se crea un producto con stock limitado y se intenta registrar una venta con una cantidad
    mayor a la disponible, verificando que se lance el error adecuado.

    Raises:
        StockInsuficienteError: Si el stock disponible es insuficiente para la venta.
    """
    # Usar base de datos en memoria
    db = SQLiteDatabase(":memory:")
    db.connect()
    db.create_tables()
    
    inventario = Inventario(db)
    producto = Producto(1, "lapiz", 500, 1, "escolar", 1)
    inventario.agregar_producto(producto)
    productos_vendidos = [(producto.to_dict(), 2)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, inventario)
    gestor_ventas = Tienda(inventario)

    with pytest.raises(StockInsuficienteError, match="Stock insuficiente para el producto lapiz"):
        gestor_ventas.registrar_venta(venta, inventario)
    
    db.disconnect()


def test_venta_cantidad_negativa():
    """
    Test para verificar que una venta con una cantidad negativa de productos lance 
    el error `VentaInvalidaError`.

    Se crea una venta con una cantidad negativa de productos y se verifica que se lance 
    el error adecuado con el mensaje correspondiente.

    Raises:
        VentaInvalidaError: Si la cantidad de productos en la venta es negativa.
    """
    # Usar base de datos en memoria
    db = SQLiteDatabase(":memory:")
    db.connect()
    db.create_tables()
    
    inventario = Inventario(db)
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario.agregar_producto(producto)
    productos_vendidos = [(producto.to_dict(), -5)]
    
    with pytest.raises(VentaInvalidaError, match="La cantidad debe ser mayor a cero"):
        Venta(1, "04/03/25", productos_vendidos, 1, inventario)
    
    db.disconnect()


def test_fecha_invalida():
    """
    Test para verificar que una fecha inválida lance el error `FechaInvalidaError`.

    Se crea una venta con una fecha inválida y se verifica que se lance el error adecuado
    con el mensaje correspondiente.

    Raises:
        FechaInvalidaError: Si la fecha de la venta es inválida.
    """
    # Usar base de datos en memoria
    db = SQLiteDatabase(":memory:")
    db.connect()
    db.create_tables()
    
    inventario = Inventario(db)
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario.agregar_producto(producto)
    productos_vendidos = [(producto.to_dict(), 2)]
    
    with pytest.raises(FechaInvalidaError, match="La fecha 32/13/25 es inválida"):
        Venta(1, "32/13/25", productos_vendidos, 1, inventario)
    
    db.disconnect()

# test caso extremo


def test_venta_producto_fantasma(inventario_limpio):
    """
    Test para verificar que si se intenta vender un producto no registrado en el inventario, 
    se lance el error `VentaProductoNoRegistradoError`.

    Se crea un producto con un ID que no está registrado en el inventario, luego se intenta 
    realizar una venta con este producto para verificar que se lance el error adecuado.

    Raises:
        VentaProductoNoRegistradoError: Si el producto no está registrado en el inventario.
    """
    producto = Producto(99, "No existe", 100, 1, "Fantasma", 1)
    productos_vendidos = [(producto.to_dict(), 1)]
    with pytest.raises(VentaProductoNoRegistradoError):
        Venta(7, "04/03/25", productos_vendidos, 1, inventario_limpio)


def test_descuento_excesivo(inventario_limpio):
    """
    Test para verificar que un descuento excesivo lance el error `DescuentoInvalidoError`.

    Se crea una venta con un descuento del 150%, lo que es inválido. Se verifica que se lance
    el error adecuado con el mensaje correspondiente.

    Raises:
        DescuentoInvalidoError: Si el descuento es mayor al 100%.
    """
    producto = Producto(1, "lapiz", 10, 1, "escolar", 1)
    productos_vendidos = [(producto.to_dict(), 2)]
    inventario = inventario_limpio
    inventario.agregar_producto(producto)
    venta = Venta(1, "04/03/25", productos_vendidos, 100, inventario)

    with pytest.raises(DescuentoInvalidoError):
        venta.aplicar_descuento(150)  # 150% de descuento


def test_venta_sin_productos(inventario_limpio):
    """
    Test para verificar que una venta sin productos lance el error `VentaInvalidaError`.

    Se crea una venta sin productos vendidos y se verifica que se lance el error adecuado 
    con el mensaje correspondiente.

    Raises:
        VentaInvalidaError: Si no se incluyen productos en la venta.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    productos_vendidos = []
    inventario_limpio.agregar_producto(producto)
    with pytest.raises(VentaInvalidaError):
        Venta(9, "04/03/25", productos_vendidos, 1, inventario_limpio)


def test_registrar_venta_stock_insuficiente2(inventario_limpio):
    """
    Test para verificar que si se intenta registrar una venta con más productos de los disponibles 
    en stock, se lance el error `StockInsuficienteError`.

    Se crea un producto con un stock limitado y se intenta realizar una venta con una cantidad mayor 
    que la disponible, verificando que se lance el error adecuado.

    Raises:
        StockInsuficienteError: Si la cantidad de productos vendidos excede el stock disponible.
    """
    gestor_ventas = Tienda(inventario_limpio)

    producto = Producto(1, "lapiz", 500, 1, "escolar", 5)  # Solo hay 5 en stock
    inventario_limpio.agregar_producto(producto)

    productos_vendidos = [(producto.to_dict(), 10)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, inventario_limpio)
    with pytest.raises(StockInsuficienteError, match="Stock insuficiente para el producto lapiz"):
        gestor_ventas.registrar_venta(venta, inventario_limpio)


def test_venta_sin_empleado(inventario_limpio):
    """
    Test para verificar que una venta sin un empleado asignado lance el error `VentaSinEmpleadoError`.

    Se crea una venta sin un empleado asignado y se verifica que se lance el error adecuado.

    Raises:
        VentaSinEmpleadoError: Si la venta no tiene un empleado asignado.
    """
    producto = Producto(6, "Mouse", 30, 1, "electronica", 1)  # ✅ "electronica" (sin tilde)
    productos_vendidos = [(producto.to_dict(), 30)]
    inventario_limpio.agregar_producto(producto)
    with pytest.raises(VentaSinEmpleadoError):
        Venta(15, "04/03/25", productos_vendidos, None, inventario_limpio)


def test_venta_producto_categoria_invalida(inventario_limpio):
    """
    Test para verificar que una venta con un producto de categoría inválida lance el error 
    `CategoriaInvalidaError`.

    Se crea un producto con una categoría no registrada y se intenta realizar una venta con 
    ese producto para verificar que se lance el error adecuado.

    Raises:
        CategoriaInvalidaError: Si el producto tiene una categoría no válida.
    """
    producto = Producto(8, "Cámara", 500, 1, "Categoría Fantasma", 1)  # Categoría inexistente
    productos_vendidos = [(producto.to_dict(), 500)]
    inventario_limpio.agregar_producto(producto)
    with pytest.raises(CategoriaInvalidaError):
        Venta(17, "04/03/25", productos_vendidos, 1, inventario_limpio)
