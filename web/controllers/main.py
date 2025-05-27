"""
Controlador principal de la interfaz web.
Gestiona la ruta raíz y la redirección según el estado de sesión y el rol del usuario.
"""
from flask import Blueprint, render_template, redirect, url_for, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    Ruta principal que redirige al login si no hay sesión activa,
    o al dashboard correspondiente según el rol del usuario.
    """
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    # Redirigir según el rol del usuario
    if session.get('user_role') == 'admin':
        return redirect(url_for('usuarios.index'))
    elif session.get('user_role') == 'vendedor':
        return redirect(url_for('ventas.index'))
    else:  # inventarista
        return redirect(url_for('productos.index')) 