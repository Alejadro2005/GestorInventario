"""
Controlador de ventas para la interfaz web.
Gestiona las rutas y vistas relacionadas con la administración de ventas.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from modelos.venta import Venta
from database.postgres_database import PostgresDatabase
from database.database_config import DatabaseConfig
from datetime import datetime

ventas_bp = Blueprint('ventas', __name__)

# Diccionario temporal en memoria para métodos de pago
metodos_pago_temporales = {}

@ventas_bp.route('/ventas')
def index():
    """
    Muestra la lista de ventas registradas en el sistema, incluyendo productos y método de pago.
    """
    try:
        ventas = g.db.get_all_sales()
        for venta in ventas:
            detalles = g.db.get_sale_details(venta['id'])
            productos_legibles = []
            for det in detalles:
                producto = g.db.get_product(det['producto_id'])
                if producto:
                    productos_legibles.append(f"{producto['nombre']} ({det['cantidad']})")
            venta['productos_legibles'] = ', '.join(productos_legibles)
            # Mostrar método de pago si está en memoria, si no 'No disponible'
            venta['metodo_pago'] = metodos_pago_temporales.get(venta['id'], 'No disponible')
            venta['fecha_hora'] = venta['fecha']
        return render_template('ventas/index.html', ventas=ventas)
    except Exception as e:
        flash(f'Error al obtener ventas: {str(e)}', 'error')
        return render_template('ventas/index.html', ventas=[])

@ventas_bp.route('/ventas/crear', methods=['GET', 'POST'])
def crear():
    """
    Permite crear una nueva venta mediante un formulario web.
    Realiza validaciones, descuenta stock y muestra mensajes de error o éxito.
    """
    productos = g.db.get_all_products()
    if request.method == 'POST':
        try:
            detalles = []
            total = 0
            for producto in productos:
                checkbox = request.form.get(f'producto_{producto["id"]}')
                cantidad_str = request.form.get(f'cantidad_{producto["id"]}')
                if checkbox and cantidad_str and cantidad_str.isdigit():
                    cantidad = int(cantidad_str)
                    if cantidad > 0:
                        total += producto['precio'] * cantidad
                        detalles.append({
                            'producto_id': producto['id'],
                            'cantidad': cantidad,
                            'precio': producto['precio']
                        })
            if not detalles:
                flash('Debes seleccionar al menos un producto y su cantidad.', 'error')
                return render_template('ventas/crear.html', productos=productos)
            venta_data = {
                'id_usuario': int(request.form['id_usuario']),
                'fecha': datetime.now(),
                'total': total
            }
            venta_id = g.db.create_sale(venta_data)
            # Guardar método de pago en memoria temporal
            metodos_pago_temporales[venta_id] = request.form.get('metodo_pago', 'No disponible')
            for detalle in detalles:
                detalle_data = {
                    'venta_id': venta_id,
                    'producto_id': detalle['producto_id'],
                    'cantidad': detalle['cantidad'],
                    'precio': detalle['precio']
                }
                g.db.insert_sale_detail(detalle_data)
                producto_actual = g.db.get_product(detalle['producto_id'])
                if producto_actual:
                    nuevo_stock = producto_actual['cantidad'] - detalle['cantidad']
                    g.db.update_stock(detalle['producto_id'], nuevo_stock)
            flash('Venta creada exitosamente', 'success')
            return redirect(url_for('ventas.index'))
        except Exception as e:
            flash(f'Error al crear venta: {str(e)}', 'error')
    return render_template('ventas/crear.html', productos=productos)

@ventas_bp.route('/ventas/<int:id>/actualizar', methods=['GET', 'POST'])
def actualizar(id):
    """
    Permite actualizar los datos de una venta existente.
    Realiza validaciones, actualiza detalles y stock, y muestra mensajes de error o éxito.
    """
    productos = g.db.get_all_products()
    if request.method == 'POST':
        try:
            productos_seleccionados = request.form.getlist('productos')
            detalles = []
            total = 0
            for prod_id in productos_seleccionados:
                cantidad = int(request.form.get(f'cantidad_{prod_id}', 0))
                producto = g.db.get_product(int(prod_id))
                if producto and cantidad > 0:
                    total += producto['precio'] * cantidad
                    detalles.append({
                        'producto_id': producto['id'],
                        'cantidad': cantidad,
                        'precio': producto['precio']
                    })
            venta_data = {
                'id_usuario': int(request.form['id_usuario']),
                'fecha': datetime.now(),
                'total': total
            }
            # Eliminar detalles anteriores
            g.db.delete_sale(id)
            # Crear nueva venta con el mismo id
            venta_data['id'] = id
            g.db.create_sale(venta_data)
            for detalle in detalles:
                detalle_data = {
                    'venta_id': id,
                    'producto_id': detalle['producto_id'],
                    'cantidad': detalle['cantidad'],
                    'precio': detalle['precio']
                }
                g.db.insert_sale_detail(detalle_data)
                # Actualizar stock
                producto = g.db.get_product(detalle['producto_id'])
                if producto:
                    nuevo_stock = producto['cantidad'] - detalle['cantidad']
                    g.db.update_stock(detalle['producto_id'], nuevo_stock)
            flash('Venta actualizada exitosamente', 'success')
            return redirect(url_for('ventas.index'))
        except Exception as e:
            flash(f'Error al actualizar venta: {str(e)}', 'error')
    try:
        venta = g.db.get_sale(id)
        detalles = g.db.get_sale_details(id)
        detalles_dict = {d['producto_id']: d['cantidad'] for d in detalles}
        if venta:
            return render_template('ventas/actualizar.html', venta=venta, productos=productos, detalles=detalles_dict)
        flash('Venta no encontrada', 'error')
        return redirect(url_for('ventas.index'))
    except Exception as e:
        flash(f'Error al obtener venta: {str(e)}', 'error')
        return redirect(url_for('ventas.index'))

@ventas_bp.route('/ventas/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    """
    Elimina una venta del sistema y muestra mensajes de éxito o error.
    """
    try:
        g.db.delete_sale(id)
        flash('Venta eliminada exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar venta: {str(e)}', 'error')
    return redirect(url_for('ventas.index'))

@ventas_bp.route('/ventas/<int:id>/deshacer', methods=['POST'])
def deshacer(id):
    """
    Deshace una venta, restaurando el stock de los productos y eliminando la venta.
    """
    try:
        # Obtener detalles de la venta
        detalles = g.db.get_sale_details(id)
        # Restaurar stock de cada producto
        for detalle in detalles:
            producto = g.db.get_product(detalle['producto_id'])
            if producto:
                nuevo_stock = producto['cantidad'] + detalle['cantidad']
                g.db.update_stock(detalle['producto_id'], nuevo_stock)
        # Eliminar la venta y sus detalles
        g.db.delete_sale(id)
        flash('Venta deshecha y stock restaurado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al deshacer venta: {str(e)}', 'error')
    return redirect(url_for('ventas.index')) 