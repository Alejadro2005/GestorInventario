"""
Controlador de usuarios para la interfaz web.
Gestiona las rutas y vistas relacionadas con la administración de usuarios.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, g, session
from modelos.usuario import Usuario
from database.postgres_database import PostgresDatabase
from database.database_config import DatabaseConfig

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.before_request
def solo_admin():
    """
    Restringe el acceso a las rutas de usuarios solo al usuario administrador.
    """
    if session.get('user_role') != 'admin':
        flash('Solo el administrador puede acceder a esta sección.', 'error')
        return redirect(url_for('ventas.index'))

@usuarios_bp.route('/usuarios')
def index():
    """
    Muestra la lista de usuarios registrados en el sistema.
    """
    try:
        usuarios = g.db.get_all_users()
        return render_template('usuarios/index.html', usuarios=usuarios)
    except Exception as e:
        flash(f'Error al obtener usuarios: {str(e)}', 'error')
        return render_template('usuarios/index.html', usuarios=[])

@usuarios_bp.route('/usuarios/crear', methods=['GET', 'POST'])
def crear():
    """
    Permite crear un nuevo usuario mediante un formulario web.
    Realiza validaciones y muestra mensajes de error o éxito.
    """
    if request.method == 'POST':
        try:
            nombre = request.form['nombre'].strip()
            rol = request.form['rol'].strip().lower()
            password = request.form['contrasena'].strip()
            # Validaciones igual que en Kivy
            if not nombre or not rol or not password:
                raise ValueError("Todos los campos son obligatorios")
            if len(nombre) < 3:
                raise ValueError("El nombre debe tener al menos 3 caracteres")
            if len(password) < 6:
                raise ValueError("La contraseña debe tener al menos 6 caracteres")
            if rol not in ["admin", "empleado"]:
                raise ValueError("El rol debe ser 'admin' o 'empleado'")
            usuario_data = {
                'nombre': nombre,
                'rol': rol,
                'password': password
            }
            g.db.create_user(usuario_data)
            flash('Usuario creado exitosamente', 'success')
            return redirect(url_for('usuarios.index'))
        except Exception as e:
            flash(f'Error al crear usuario: {str(e)}', 'error')
    return render_template('usuarios/crear.html')

@usuarios_bp.route('/usuarios/<int:id>/actualizar', methods=['GET', 'POST'])
def actualizar(id):
    """
    Permite actualizar los datos de un usuario existente.
    Realiza validaciones y muestra mensajes de error o éxito.
    """
    if request.method == 'POST':
        try:
            nombre = request.form['nombre'].strip()
            rol = request.form['rol'].strip().lower()
            password = request.form['contrasena'].strip()
            # Validaciones igual que en Kivy
            if not nombre or not rol or not password:
                raise ValueError("Todos los campos son obligatorios")
            if len(nombre) < 3:
                raise ValueError("El nombre debe tener al menos 3 caracteres")
            if len(password) < 6:
                raise ValueError("La contraseña debe tener al menos 6 caracteres")
            if rol not in ["admin", "empleado"]:
                raise ValueError("El rol debe ser 'admin' o 'empleado'")
            usuario_data = {
                'nombre': nombre,
                'rol': rol,
                'password': password
            }
            g.db.update_user(id, usuario_data)
            flash('Usuario actualizado exitosamente', 'success')
            return redirect(url_for('usuarios.index'))
        except Exception as e:
            flash(f'Error al actualizar usuario: {str(e)}', 'error')
    
    try:
        usuario = g.db.get_user(id)
        if usuario:
            return render_template('usuarios/actualizar.html', usuario=usuario)
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('usuarios.index'))
    except Exception as e:
        flash(f'Error al obtener usuario: {str(e)}', 'error')
        return redirect(url_for('usuarios.index'))

@usuarios_bp.route('/usuarios/<int:id>/eliminar', methods=['POST'])
def eliminar(id):
    """
    Elimina un usuario del sistema si no está asociado a ventas.
    Muestra mensajes de advertencia o éxito.
    """
    try:
        g.db.delete_user(id)
        flash('Usuario eliminado exitosamente', 'success')
    except Exception as e:
        msg = str(e)
        if 'llave foránea' in msg or 'foreign key' in msg:
            flash('No se puede eliminar el usuario porque está asociado a ventas registradas.', 'error')
        else:
            flash(f'Error al eliminar usuario: {msg}', 'error')
    return redirect(url_for('usuarios.index')) 