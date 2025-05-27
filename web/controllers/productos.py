"""
Controlador de productos para la interfaz web.
Gestiona las rutas y vistas relacionadas con la administración de productos.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session
from modelos.producto import Producto
from database.postgres_database import PostgresDatabase
from database.database_config import DatabaseConfig

productos_bp = Blueprint('productos', __name__)

@productos_bp.before_request
def solo_admin():
    """
    Restringe el acceso a las rutas de productos solo al usuario administrador.
    """
    if session.get('user_role') != 'admin':
        flash('Solo el administrador puede acceder a esta sección.', 'error')
        return redirect(url_for('ventas.index'))

@productos_bp.route('/productos')
def index():
    """
    Muestra la lista de productos registrados en el sistema.
    """
    try:
        productos = g.db.get_all_products()
        return render_template('productos/index.html', productos=productos)
    except Exception as e:
        flash(f'Error al obtener productos: {str(e)}', 'error')
        return render_template('productos/index.html', productos=[])

@productos_bp.route('/productos/crear', methods=['GET', 'POST'])
def crear():
    """
    Permite crear un nuevo producto mediante un formulario web.
    Realiza validaciones y muestra mensajes de error o éxito.
    """
    if request.method == 'POST':
        try:
            nombre = request.form['nombre'].strip()
            precio = float(request.form['precio'])
            cantidad = int(request.form['cantidad'])
            categoria = request.form['categoria'].strip().lower()
            stock_minimo = int(request.form['stock_minimo'])
            # Validaciones igual que en Kivy
            if not nombre or not categoria:
                raise ValueError("Todos los campos son obligatorios")
            if len(nombre) < 3:
                raise ValueError("El nombre del producto debe tener al menos 3 caracteres")
            if precio <= 0:
                raise ValueError("El precio debe ser mayor que cero")
            if cantidad < 0:
                raise ValueError("La cantidad no puede ser negativa")
            if cantidad > 1000:
                raise ValueError("La cantidad no puede ser mayor a 1000")
            if stock_minimo < 0:
                raise ValueError("El stock mínimo no puede ser negativo")
            if stock_minimo > 1000:
                raise ValueError("El stock mínimo no puede ser mayor a 1000")
            if categoria not in ['electronica', 'escolar']:
                raise ValueError("La categoría debe ser 'electronica' o 'escolar'")
            producto_data = {
                'nombre': nombre,
                'precio': precio,
                'cantidad': cantidad,
                'categoria': categoria,
                'stock_minimo': stock_minimo
            }
            g.db.create_product(producto_data)
            flash('Producto creado exitosamente', 'success')
            return redirect(url_for('productos.index'))
        except Exception as e:
            flash(f'Error al crear producto: {str(e)}', 'error')
    return render_template('productos/crear.html')

@productos_bp.route('/productos/<int:id>/actualizar', methods=['GET', 'POST'])
def actualizar(id):
    """
    Permite actualizar los datos de un producto existente.
    Realiza validaciones y muestra mensajes de error o éxito.
    """
    if request.method == 'POST':
        try:
            nombre = request.form['nombre'].strip()
            precio = float(request.form['precio'])
            cantidad = int(request.form['cantidad'])
            categoria = request.form['categoria'].strip().lower()
            stock_minimo = int(request.form['stock_minimo'])
            # Validaciones igual que en Kivy
            if not nombre or not categoria:
                raise ValueError("Todos los campos son obligatorios")
            if len(nombre) < 3:
                raise ValueError("El nombre del producto debe tener al menos 3 caracteres")
            if precio <= 0:
                raise ValueError("El precio debe ser mayor que cero")
            if cantidad < 0:
                raise ValueError("La cantidad no puede ser negativa")
            if cantidad > 1000:
                raise ValueError("La cantidad no puede ser mayor a 1000")
            if stock_minimo < 0:
                raise ValueError("El stock mínimo no puede ser negativo")
            if stock_minimo > 1000:
                raise ValueError("El stock mínimo no puede ser mayor a 1000")
            if categoria not in ['electronica', 'escolar']:
                raise ValueError("La categoría debe ser 'electronica' o 'escolar'")
            producto_data = {
                'nombre': nombre,
                'precio': precio,
                'cantidad': cantidad,
                'categoria': categoria,
                'stock_minimo': stock_minimo
            }
            g.db.update_product(id, producto_data)
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('productos.index'))
        except Exception as e:
            flash(f'Error al actualizar producto: {str(e)}', 'error')
    
    try:
        producto = g.db.get_product(id)
        if producto:
            return render_template('productos/actualizar.html', producto=producto)
        flash('Producto no encontrado', 'error')
        return redirect(url_for('productos.index'))
    except Exception as e:
        flash(f'Error al obtener producto: {str(e)}', 'error')
        return redirect(url_for('productos.index'))

@productos_bp.route('/productos/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    """
    Elimina un producto del sistema si no está asociado a ventas.
    Muestra mensajes de advertencia o éxito.
    """
    try:
        # Verificar si el producto está asociado a alguna venta
        detalles = g.db.get_all_sale_details()
        asociado = any(det['producto_id'] == id for det in detalles)
        if asociado:
            flash('No se puede eliminar este producto porque está asociado a una o más ventas. Si deseas eliminarlo, primero elimina las ventas asociadas.', 'warning')
        else:
            g.db.delete_product(id)
            flash('Producto eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar producto: {str(e)}', 'error')
    return redirect(url_for('productos.index')) 