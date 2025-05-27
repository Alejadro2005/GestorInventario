"""
Controlador de historial de ventas para la interfaz web.
Gestiona las rutas y vistas relacionadas con el historial de ventas.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from database.postgres_database import PostgresDatabase
from database.database_config import DatabaseConfig

historial_bp = Blueprint('historial', __name__)

@historial_bp.route('/historial')
def index():
    """
    Muestra el historial de ventas, incluyendo productos vendidos y cantidades.
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
        return render_template('historial/index.html', ventas=ventas)
    except Exception as e:
        flash(f'Error al obtener historial: {str(e)}', 'error')
        return render_template('historial/index.html', ventas=[])

@historial_bp.route('/historial/eliminar', methods=['POST'])
def eliminar():
    """
    Elimina todo el historial de ventas del sistema y muestra mensajes de éxito o error.
    """
    try:
        g.db.delete_all_sales()
        flash('Historial eliminado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al eliminar historial: {str(e)}', 'error')
    return redirect(url_for('historial.index')) 