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
from src.errores.stock_invalido import StockInvalidoError
from src.database.test_database import DatabaseTest

@pytest.fixture
def db():
    db = DatabaseTest()
    db.connect()
    db.create_tables()
    yield db
    db.disconnect()

@pytest.fixture
def inventario(db):
    return Inventario(db)

@pytest.fixture
def inventario_limpio():
    db = DatabaseTest()
    db.connect()
    db.create_tables()
    def get_next_sale_id(self):
        ventas = self.get_all_sales()
        if ventas:
            return max(v['id'] for v in ventas) + 1
        return 1
    db.get_next_sale_id = get_next_sale_id.__get__(db)
    yield Inventario(db)
    db.disconnect()

def test_registrar_venta1(inventario_limpio):
    """
    Test para verificar que se pueda registrar una venta con múltiples productos
    y que se agregue correctamente al historial de ventas.
    """
    producto1 = Producto(1, "lapiz", 500, 1, "escolar", 10)
    producto2 = Producto(2, "cuaderno", 1500, 2, "escolar", 10)
    gestor_inventario = inventario_limpio
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)
    productos_vendidos = [(producto1.to_dict(), 1), (producto2.to_dict(), 2)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, gestor_inventario)
    gestor_ventas = Tienda(gestor_inventario.db, gestor_inventario)
    venta_id = gestor_ventas.registrar_venta(venta, gestor_inventario)
    assert isinstance(venta_id, int)

def test_registrar_venta2(inventario_limpio):
    """
    Test para registrar varias ventas y asegurarse de que se agreguen correctamente
    al historial de ventas.
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
    gestor_ventas = Tienda(gestor_inventario.db, gestor_inventario)
    venta_id1 = gestor_ventas.registrar_venta(venta1, gestor_inventario)
    venta_id2 = gestor_ventas.registrar_venta(venta2, gestor_inventario)
    venta_id3 = gestor_ventas.registrar_venta(venta3, gestor_inventario)
    assert isinstance(venta_id1, int)
    assert isinstance(venta_id2, int)
    assert isinstance(venta_id3, int)

def test_registrar_venta3(inventario_limpio):
    """
    Test para verificar que se pueda registrar una venta con múltiples productos.
    """
    producto1 = Producto(1, "lapiz", 500, 10, "escolar", 10)
    producto2 = Producto(2, "cuaderno", 1500, 20, "escolar", 10)
    gestor_inventario = inventario_limpio
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)
    productos_vendidos = [(producto1.to_dict(), 2), (producto2.to_dict(), 1)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, gestor_inventario)
    gestor_ventas = Tienda(gestor_inventario.db, gestor_inventario)
    venta_id = gestor_ventas.registrar_venta(venta, gestor_inventario)
    assert isinstance(venta_id, int)

def test_calcular_total(inventario_limpio):
    """
    Test para verificar que se calcule correctamente el total de una venta.
    """
    producto1 = Producto(1, "lapiz", 500, 10, "escolar", 1)
    producto2 = Producto(2, "cuaderno", 1500, 20, "escolar", 1)
    gestor_inventario = inventario_limpio
    gestor_inventario.agregar_producto(producto1)
    gestor_inventario.agregar_producto(producto2)
    productos_vendidos = [(producto1.to_dict(), 2), (producto2.to_dict(), 1)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, gestor_inventario)
    assert venta.calcular_total() == 2500

def test_validar_stock_ventas(inventario_limpio):
    """
    Test para verificar la validación de stock antes de realizar una venta.
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
    tienda = Tienda(gestor_inventario, gestor_inventario)
    assert tienda.validar_stock_venta(1, venta1.productos_vendidos[0][1], gestor_inventario) == True
    assert tienda.validar_stock_venta(2, venta2.productos_vendidos[0][1], gestor_inventario) == True
    assert tienda.validar_stock_venta(3, venta3.productos_vendidos[0][1], gestor_inventario) == True

def test_generar_historial(inventario_limpio):
    """
    Test para verificar que se genere el historial de ventas correctamente.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    gestor_inventario = inventario_limpio
    gestor_inventario.agregar_producto(producto)
    producto_vendido = [(producto.to_dict(), 2)]
    venta = Venta(1, "03/04/25", producto_vendido, 1, gestor_inventario)
    gestor_venta = Tienda(gestor_inventario.db, gestor_inventario)
    venta_id = gestor_venta.registrar_venta(venta, gestor_inventario)
    assert isinstance(venta_id, int)

# tests error
def test_producto_precio_negativo():
    """
    Test para verificar que se lance una excepción al crear un producto con precio negativo.
    """
    with pytest.raises(PrecioInvalidoError):
        Producto(1, "lapiz", -500, 10, "escolar", 1)

def test_producto_stock_negativo():
    """
    Test para verificar que se lance una excepción al crear un producto con stock negativo.
    """
    with pytest.raises(StockInvalidoError):
        Producto(1, "lapiz", 500, -10, "escolar", 1)

def test_producto_duplicado(inventario_limpio):
    """
    Test para verificar que se lance una excepción al intentar agregar un producto duplicado.
    """
    producto1 = Producto(1, "lapiz", 500, 10, "escolar", 1)
    producto2 = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario_limpio.agregar_producto(producto1)
    with pytest.raises(ProductoDuplicadoError):
        inventario_limpio.agregar_producto(producto2)

def test_stock_insuficiente(inventario_limpio):
    """
    Test para verificar que se lance una excepción al intentar vender más productos de los disponibles.
    """
    producto = Producto(1, "lapiz", 500, 5, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    productos_vendidos = [(producto.to_dict(), 10)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, inventario_limpio)
    gestor_ventas = Tienda(inventario_limpio.db, inventario_limpio)
    with pytest.raises(StockInsuficienteError):
        gestor_ventas.registrar_venta(venta, inventario_limpio)

def test_venta_cantidad_negativa(inventario_limpio):
    """
    Test para verificar que se lance una excepción al intentar vender una cantidad negativa.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    productos_vendidos = [(producto.to_dict(), -2)]
    with pytest.raises(Exception):
        Venta(1, "04/03/25", productos_vendidos, 1, inventario_limpio)

def test_fecha_invalida():
    """
    Test para verificar que se lance una excepción al intentar crear una venta con fecha inválida.
    """
    with pytest.raises(Exception):
        Venta(1, "32/13/25", [], 1, None)

def test_venta_producto_fantasma(inventario_limpio):
    """
    Test para verificar que se lance una excepción al intentar vender un producto inexistente.
    """
    producto = Producto(99, "lapiz", 500, 10, "escolar", 1)
    productos_vendidos = [(producto.to_dict(), 2)]
    with pytest.raises(Exception):
        Venta(1, "04/03/25", productos_vendidos, 1, inventario_limpio)

def test_descuento_excesivo(inventario_limpio):
    """
    Test para verificar que se lance una excepción al intentar aplicar un descuento excesivo.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    productos_vendidos = [(producto.to_dict(), 2)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, inventario_limpio)
    with pytest.raises(Exception):
        venta.aplicar_descuento(200)

def test_venta_sin_productos(inventario_limpio):
    """
    Test para verificar que se lance una excepción al intentar crear una venta sin productos.
    """
    with pytest.raises(Exception):
        Venta(1, "04/03/25", [], 1, inventario_limpio)

def test_registrar_venta_stock_insuficiente2(inventario_limpio):
    """
    Test para verificar que se lance una excepción al intentar registrar una venta con stock insuficiente.
    """
    gestor_ventas = Tienda(inventario_limpio, inventario_limpio)
    producto = Producto(1, "lapiz", 500, 5, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    productos_vendidos = [(producto.to_dict(), 10)]
    venta = Venta(1, "04/03/25", productos_vendidos, 1, inventario_limpio)
    with pytest.raises(StockInsuficienteError):
        gestor_ventas.registrar_venta(venta, inventario_limpio)

def test_venta_sin_empleado(inventario_limpio):
    """
    Test para verificar que se lance una excepción al intentar crear una venta sin empleado.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    productos_vendidos = [(producto.to_dict(), 2)]
    with pytest.raises(Exception):
        Venta(1, "04/03/25", productos_vendidos, None, inventario_limpio)

def test_venta_producto_categoria_invalida():
    """
    Test para verificar que se lance una excepción al intentar crear un producto con categoría inválida.
    """
    with pytest.raises(CategoriaInvalidaError):
        Producto(1, "lapiz", 500, 10, "", 1)
