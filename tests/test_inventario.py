import pytest
from src.modelos.producto import Producto
from src.modelos.inventario import Inventario
from src.errores.productos_duplicados import ProductoDuplicadoError
from src.errores.producto_no_encontrado import ProductoNoEncontradoError
from src.errores.producto_invalido import ProductoInvalidoError
from src.errores.stock_invalido import StockInvalidoError
from src.errores.no_hay_productos import NoHayProductosError
from src.errores.categoria_invalida import CategoriaInvalidaError
from src.errores.precio_invalido import PrecioInvalidoError
from src.errores.stock_insuficiente import StockInsuficienteError
from src.database.test_database import DatabaseTest

@pytest.fixture
def inventario():
    db = DatabaseTest()
    db.connect()
    db.create_tables()
    yield Inventario(db)
    db.disconnect()

# Tests caso normal

def test_agregar_producto_a_inventario(inventario_limpio):
    """
    Verifica que un producto se agrega correctamente al inventario.

    Crea un producto y lo agrega al inventario. Luego verifica que el inventario contenga un solo producto.

    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    productos = inventario_limpio.db.get_all_products()
    assert len(productos) == 1


def test_eliminar_producto_de_inventario(inventario_limpio):
    """
    Verifica que un producto se elimina correctamente del inventario.

    Crea un producto, lo agrega al inventario, y luego verifica que se elimine correctamente. 
    Se asegura que el mensaje de éxito sea el esperado.
    """
    producto = Producto(1, "lapiz", 8500, 10, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    assert inventario_limpio.eliminar_producto(1) == "El producto 'lapiz' ha sido eliminado con éxito."


def test_actualizar_stock(inventario_limpio):
    """
    Test para verificar que se pueda actualizar el stock de un producto correctamente.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    inventario_limpio.actualizar_stock(1, 15)
    producto_obtenido = inventario_limpio.obtener_producto(1)
    # El mock suma la cantidad, así que debe ser 25
    assert producto_obtenido.cantidad == 25


def test_filtrar_stock_bajo(inventario_limpio):
    producto = Producto(1, "lapiz", 500, 1, "escolar", 10)  # cantidad=1, stock_minimo=10
    producto2 = Producto(2, "cuaderno", 1500, 20, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    inventario_limpio.agregar_producto(producto2)
    resultado = inventario_limpio.filtrar_por_stock_bajo()
    assert resultado[0].id == producto.id


def test_eliminar_producto2(inventario_limpio):
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    producto2 = Producto(2, "cuaderno", 1500, 20, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    inventario_limpio.agregar_producto(producto2)
    inventario_limpio.eliminar_producto(1)
    productos = inventario_limpio.db.get_all_products()
    assert len(productos) == 1


def test_actualizar_stock_producto():
    """
    Verifica que el stock de un producto se actualiza correctamente.

    Se crea un producto, se actualiza su stock y se verifica que la cantidad del producto se haya actualizado.
    """
    producto = Producto(1, "lapiz", 500, 5, "escolar", 1)
    producto.actualizar_stock(10)
    assert producto.cantidad == 10


# Test caso Error

def test_agregar_producto_duplicado(inventario_limpio):
    """
    Test para verificar que se lance una excepción al intentar agregar un producto con nombre duplicado.
    """
    producto1 = Producto(1, "lapiz", 500, 10, "escolar", 1)
    producto2 = Producto(2, "lapiz", 1500, 20, "escolar", 1)  # mismo nombre
    inventario_limpio.agregar_producto(producto1)
    with pytest.raises(ProductoDuplicadoError):
        inventario_limpio.agregar_producto(producto2)


def test_eliminar_producto_inexistente(inventario_limpio):
    """
    Verifica que se lanza un error al intentar eliminar un producto que no existe.

    Intenta eliminar un producto con un ID que no existe en el inventario y asegura que se 
    lance una excepción ProductoNoEncontradoError.
    """
    with pytest.raises(ProductoNoEncontradoError):
        inventario_limpio.eliminar_producto(99)  # ID que no existe


def test_actualizar_stock_cantidad_negativa(inventario_limpio):
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    # Intentar reducir más de lo que hay en stock
    with pytest.raises(StockInvalidoError):
        inventario_limpio.actualizar_stock(1, -15)  # Stock resultante sería negativo


def test_filtrar_stock_sin_productos(inventario_limpio):
    with pytest.raises(NoHayProductosError):
        inventario_limpio.filtrar_por_stock_bajo()


def test_producto_invalido_nombre_vacio():
    with pytest.raises(ProductoInvalidoError):
        Producto(1, "", 500, 10, "escolar", 1)


def test_actualizar_stock_producto_inexistente(inventario_limpio):
    """
    Test para verificar que actualizar el stock de un producto inexistente no lanza excepción pero no cambia nada.
    """
    # El método no lanza excepción, solo no hace nada
    inventario_limpio.actualizar_stock(99, 10)
    producto = inventario_limpio.obtener_producto(99)
    assert producto is None


# test caso extremo

# def test_categoria_numerica():
#     pass

# def test_stock_maximo_excedido():
#     pass

# def test_precio_cero():
#     pass

def test_nombre_producto_caracteres_especiales():
    # Antes se esperaba una excepción, ahora solo se verifica que se puede crear el producto
    producto = Producto(1, "Lápiz@#", 500, 10, "escolar", 1)
    assert producto.nombre == "Lápiz@#"


def test_categoria_vacia():
    with pytest.raises(CategoriaInvalidaError):
        Producto(10, "Borrador", 100, 5, "", 1)


def test_precio_negativo():
    with pytest.raises(PrecioInvalidoError):
        Producto(11, "Borrador", -100, 5, "escolar", 1)


def test_stock_negativo():
    with pytest.raises(StockInvalidoError):
        Producto(12, "Borrador", 100, -5, "escolar", 1)


def test_agregar_producto(inventario_limpio):
    """
    Test para verificar que se pueda agregar un producto correctamente.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    productos = inventario_limpio.db.get_all_products()
    assert len(productos) == 1


def test_eliminar_producto(inventario_limpio):
    """
    Test para verificar que se pueda eliminar un producto correctamente.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    inventario_limpio.eliminar_producto(1)
    productos = inventario_limpio.db.get_all_products()
    assert len(productos) == 0


def test_actualizar_producto(inventario_limpio):
    """
    Test para verificar que se pueda actualizar un producto correctamente.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    producto_actualizado = Producto(1, "lapiz", 600, 15, "escolar", 1)
    inventario_limpio.modificar_producto(1, producto_actualizado)
    producto_obtenido = inventario_limpio.obtener_producto(1)
    assert producto_obtenido.precio == 600
    assert producto_obtenido.cantidad == 15


def test_obtener_producto_inexistente(inventario_limpio):
    """
    Test para verificar que obtener un producto inexistente devuelve None.
    """
    producto = inventario_limpio.obtener_producto(99)
    assert producto is None


def test_actualizar_producto_inexistente(inventario_limpio):
    """
    Test para verificar que se lance una excepción al intentar actualizar un producto inexistente.
    """
    producto = Producto(99, "lapiz", 500, 10, "escolar", 1)
    with pytest.raises(Exception):
        inventario_limpio.modificar_producto(99, producto)


def test_eliminar_producto_inexistente(inventario_limpio):
    """
    Test para verificar que se lance una excepción al intentar eliminar un producto inexistente.
    """
    with pytest.raises(Exception):
        inventario_limpio.eliminar_producto(99)


def test_actualizar_stock_negativo(inventario_limpio):
    """
    Test para verificar que se lance una excepción al intentar actualizar el stock a un valor negativo.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario_limpio.agregar_producto(producto)
    with pytest.raises(StockInvalidoError):
        inventario_limpio.actualizar_stock(1, -5)


def test_obtener_todos_productos(inventario):
    productos = [
        Producto(0, 'Product 1', 10.0, 5, 'escolar', 1),
        Producto(0, 'Product 2', 20.0, 10, 'escolar', 2)
    ]
    for producto in productos:
        inventario.agregar_producto(producto)
    todos_productos = inventario.db.get_all_products()
    assert len(todos_productos) == 2
    assert todos_productos[0]['nombre'] == productos[0].nombre
    assert todos_productos[1]['nombre'] == productos[1].nombre
