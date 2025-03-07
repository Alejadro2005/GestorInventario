#test_usuarios
import pytest
from src.modelos.usuario import Usuario
from src.modulos.gestor_usuarios import GestorUsuarios
from src.errores.usuario_duplicado import UsuarioDuplicadoError
from src.errores.usuario_no_encontrado import UsuarioNoEncontradoError
from src.errores.credenciales_invalidas import CredencialesInvalidasError
from src.errores.contrasena_invalida import ContraseñaInvalidaError
from src.errores.rol_invalido import RolInvalidoError
from src.errores.nombre_usuario_invalido import NombreUsuarioInvalidoError
from src.errores.contrasena_expirada import ContraseñaExpiradaError


def test_crear_usuario():
    gestor_usuario=GestorUsuarios()
    usuario=Usuario(1,"jose","empleado","1234")
    assert gestor_usuario.crear_usuario(usuario) == "el usuario se creo con exito"

def test_usuario_validar_rol():
    gestor_usuario=GestorUsuarios()
    usuario=Usuario(1,"jose","empleado","1234")
    gestor_usuario.crear_usuario(usuario)
    assert gestor_usuario.validar_rol(1,"empleado")==True


def test_eliminar_usuario3():
    gestor_usuario=GestorUsuarios()
    usuario=Usuario(1,"jose","empleado","1234")
    usuario2=Usuario(2,"alejandro","empleado","4321")
    usuario3=Usuario(3,"pepe","empleado","9876")
    gestor_usuario.crear_usuario(usuario)
    gestor_usuario.crear_usuario(usuario2)
    gestor_usuario.crear_usuario(usuario3)
    assert gestor_usuario.eliminar_usuario(3)=="el usuario pepe ha sido eliminado"


def test_iniciar_sesion():
    usuario=Usuario(1,"jose","empleado","1234")
    assert usuario.iniciar_sesion("1234")==True


def test_cambiar_contraseña():
    usuario=Usuario(1,"jose","empleado","1234")
    assert usuario.cambiar_contraseña("4321")== "4321"


def test_iniciar_sesion2():
    usuario=Usuario(1,"jose","empleado","1234")
    assert usuario.iniciar_sesion("4321")==False
    

#Tests Error
def test_crear_usuario_duplicado():
    gestor_usuario = GestorUsuarios()
    usuario = Usuario(1, "jose", "empleado", "1234")
    gestor_usuario.crear_usuario(usuario)

    with pytest.raises(UsuarioDuplicadoError, match="El usuario con ID 1 ya existe"):
        gestor_usuario.crear_usuario(usuario)


def test_validar_rol_usuario_no_existente():
    gestor_usuario = GestorUsuarios()

    with pytest.raises(UsuarioNoEncontradoError, match="El usuario con ID 99 no existe"):
        gestor_usuario.validar_rol(99, "empleado")


def test_eliminar_usuario_inexistente():
    gestor_usuario = GestorUsuarios()

    with pytest.raises(UsuarioNoEncontradoError, match="El usuario con ID 99 no existe"):
        gestor_usuario.eliminar_usuario(99)


def test_crear_usuario_contraseña_invalida():
    with pytest.raises(ContraseñaInvalidaError, match="La contraseña no cumple con los requisitos mínimos"):
        Usuario(1, "jose", "empleado", "")


def test_iniciar_sesion_fallida():
    usuario = Usuario(1, "jose", "empleado", "1234")

    with pytest.raises(CredencialesInvalidasError, match="Credenciales incorrectas"):
        usuario.iniciar_sesion("0000")


def test_cambiar_contraseña_invalida():
    usuario = Usuario(1, "jose", "empleado", "1234")

    with pytest.raises(ContraseñaInvalidaError, match="La contraseña no cumple con los requisitos mínimos"):
        usuario.cambiar_contraseña("")

#Test caso extremo
def test_rol_con_emojis():
    with pytest.raises(RolInvalidoError):
        Usuario(8, "Ana", "admin🔥", "Pass1234")

def test_nombre_usuario_largo():
    with pytest.raises(NombreUsuarioInvalidoError):
        Usuario(9, "A"*100, "empleado", "SecurePass1")

def test_contraseña_expirada():
    usuario=Usuario(1,"jose","empleado","1234")
    with pytest.raises(ContraseñaExpiradaError):
        usuario.validar_expiracion("01/01/2020")  

def test_crear_usuario_sin_nombre():
    with pytest.raises(NombreUsuarioInvalidoError, match="El nombre de usuario no puede estar vacío"):
        Usuario(10, "", "empleado", "Pass1234")

def test_crear_usuario_con_rol_inexistente():
    with pytest.raises(RolInvalidoError, match="El rol 'superheroe' no es válido"):
        Usuario(11, "carlos", "superheroe", "Pass1234")

def test_validar_rol_usuario_eliminado():
    gestor_usuario = GestorUsuarios()
    usuario = Usuario(13, "luis", "empleado", "ClaveSegura1")

    gestor_usuario.crear_usuario(usuario)
    gestor_usuario.eliminar_usuario(13)

    with pytest.raises(UsuarioNoEncontradoError, match="El usuario con ID 13 no existe"):
        gestor_usuario.validar_rol(13, "empleado")