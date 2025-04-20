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

# Tests caso normal

def test_agregar_producto_a_inventario():
    """
    Verifica que un producto se agrega correctamente al inventario.

    Crea un producto y lo agrega al inventario. Luego verifica que el inventario contenga un solo producto.

    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario = Inventario()
    inventario.agregar_producto(producto)
    assert len(inventario.productos) == 1


def test_eliminar_producto_de_inventario():
    """
    Verifica que un producto se elimina correctamente del inventario.

    Crea un producto, lo agrega al inventario, y luego verifica que se elimine correctamente. 
    Se asegura que el mensaje de éxito sea el esperado.
    """
    producto = Producto(1, "lapiz", 8500, 10, "escolar", 1)
    inventario = Inventario()
    inventario.agregar_producto(producto)
    assert inventario.eliminar_producto(1) == "El producto 'lapiz' ha sido eliminado con éxito."


def test_actualizar_stock():
    """
    Verifica que el stock de un producto se actualiza correctamente.

    Se agrega un producto al inventario y luego se actualiza su stock. 
    Se asegura que el stock del producto se haya actualizado correctamente.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    inventario = Inventario()
    inventario.agregar_producto(producto)
    assert inventario.actualizar_stock(1, 10) == "La cantidad de 'lapiz' se ha actualizado a: 20."


def test_filtrar_stock_bajo():
    """
    Verifica que se filtran correctamente los productos con stock bajo.

    Crea dos productos, uno con stock bajo y otro con suficiente stock, 
    y luego verifica que solo el producto con stock bajo sea filtrado.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    producto2 = Producto(2, "cuaderno", 1500, 20, "escolar", 1)
    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto)
    gestor_inventario.agregar_producto(producto2)
    assert gestor_inventario.filtrar_por_stock_bajo() == [producto]


def test_eliminar_producto2():
    """
    Verifica que se elimina correctamente un producto del inventario.

    Crea dos productos, los agrega al inventario y luego elimina uno. 
    Se asegura que el inventario contenga solo el producto restante.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    producto2 = Producto(2, "cuaderno", 1500, 20, "escolar", 1)
    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto)
    gestor_inventario.agregar_producto(producto2)
    gestor_inventario.eliminar_producto(1)
    assert len(gestor_inventario.productos) == 1


def test_actualizar_stock_producto():
    """
    Verifica que el stock de un producto se actualiza correctamente.

    Se crea un producto, se actualiza su stock y se verifica que la cantidad del producto se haya actualizado.
    """
    producto = Producto(1, "lapiz", 500, 5, "escolar", 1)
    producto.actualizar_stock(5)
    assert producto.cantidad == 10


# Test caso Error

def test_agregar_producto_duplicado():
    """
    Verifica que se lanza un error al intentar agregar un producto duplicado.

    Crea un producto y lo agrega al inventario. Luego intenta agregar el mismo producto de nuevo 
    y verifica que se lance una excepción ProductoDuplicadoError.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto)
    with pytest.raises(ProductoDuplicadoError):
        gestor_inventario.agregar_producto(producto)


def test_eliminar_producto_inexistente():
    """
    Verifica que se lanza un error al intentar eliminar un producto que no existe.

    Intenta eliminar un producto con un ID que no existe en el inventario y asegura que se 
    lance una excepción ProductoNoEncontradoError.
    """
    gestor_inventario = Inventario()
    with pytest.raises(ProductoNoEncontradoError):
        gestor_inventario.eliminar_producto(99)  # ID que no existe


def test_actualizar_stock_cantidad_negativa():
    """
    Verifica que se lanza un error al intentar actualizar el stock con una cantidad negativa.

    Se intenta actualizar el stock de un producto con una cantidad negativa y se asegura que 
    se lance una excepción StockInvalidoError.
    """
    producto = Producto(1, "lapiz", 500, 10, "escolar", 1)
    gestor_inventario = Inventario()
    gestor_inventario.agregar_producto(producto)
    with pytest.raises(StockInvalidoError):
        gestor_inventario.actualizar_stock(1, -5)  # Stock negativo


def test_filtrar_stock_sin_productos():
    """
    Verifica que se lanza un error si no hay productos en el inventario al intentar filtrar productos con stock bajo.

    Se asegura que se lance una excepción NoHayProductosError cuando se intenta filtrar productos
    sin que haya productos en el inventario.
    """
    gestor_inventario = Inventario()
    with pytest.raises(NoHayProductosError):
        gestor_inventario.filtrar_por_stock_bajo()


def test_producto_invalido_nombre_vacio():
    """
    Verifica que se lanza un error al crear un producto con un nombre vacío.

    Se asegura que se lance una excepción ProductoInvalidoError si el nombre del producto está vacío.
    """
    with pytest.raises(ProductoInvalidoError):
        producto = Producto(1, "", 500, 10, "escolar", 1)  # Nombre vacío debería ser inválido


def test_actualizar_stock_producto_inexistente():
    """
    Verifica que se lanza un error al intentar actualizar el stock de un producto que no existe.

    Se asegura que se lance una excepción ProductoNoEncontradoError si se intenta actualizar el stock
    de un producto con un ID que no existe en el inventario.
    """
    gestor_inventario = Inventario()
    with pytest.raises(ProductoNoEncontradoError):
        gestor_inventario.actualizar_stock(99, 5)  # Producto con ID 99 no existe


# test caso extremo

def test_categoria_numerica():
    """
    Verifica que se lanza un error al intentar crear un producto con una categoría numérica.

    Se asegura que se lance una excepción CategoriaInvalidaError si la categoría del producto es un número.
    """
    with pytest.raises(CategoriaInvalidaError):
        Producto(3, "Bolígrafo", 300, 10, "1234", 1)


def test_stock_maximo_excedido():
    """
    Verifica que se lanza un error al intentar crear un producto con un stock mayor al máximo permitido.

    Se asegura que se lance una excepción StockInvalidoError si el stock del producto excede el límite de 1000.
    """
    with pytest.raises(StockInvalidoError):
        Producto(4, "Cuaderno", 1500, 1001, "Escolar", 10)  # Límite: 1000


def test_precio_cero():
    """
    Verifica que se lanza un error al intentar crear un producto con un precio igual a cero.

    Se asegura que se lance una excepción PrecioInvalidoError si el precio del producto es cero.
    """
    with pytest.raises(PrecioInvalidoError):
        Producto(5, "Goma", 0, 10, "Escolar", 1)


def test_precio_negativo():
    """
    Verifica que se lanza un error al intentar crear un producto con un precio negativo.

    Se asegura que se lance una excepción PrecioInvalidoError si el precio del producto es negativo.
    """
    with pytest.raises(PrecioInvalidoError):
        Producto(6, "Regla", -50, 10, "Escolar", 1)


def test_nombre_producto_caracteres_especiales():
    """
    Verifica que se lanza un error al intentar crear un producto con caracteres especiales en el nombre.

    Se asegura que se lance una excepción ProductoInvalidoError si el nombre del producto contiene caracteres especiales.
    """
    with pytest.raises(ProductoInvalidoError):
        Producto(9, "@@Lápiz!!", 500, 10, "Escolar", 1)


def test_categoria_vacia():
    """
    Verifica que se lanza un error al intentar crear un producto con una categoría vacía.

    Se asegura que se lance una excepción CategoriaInvalidaError si la categoría del producto está vacía.
    """
    with pytest.raises(CategoriaInvalidaError):
        Producto(10, "Borrador", 100, 5, "", 1)
