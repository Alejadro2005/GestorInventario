import pytest
from src.modelos.usuario import Usuario
from src.errores.contrasena_invalida import ContrasenaInvalidaError
from src.errores.credenciales_invalidas import CredencialesInvalidasError
from src.errores.rol_invalido import RolInvalidoError
from src.errores.nombre_usuario_invalido import NombreUsuarioInvalidoError
from src.errores.contrasena_expirada import ContrasenaExpiradaError

def test_crear_usuario():
    usuario = Usuario(1, "admin", "admin", "admin123")
    assert usuario.id == 1
    assert usuario.nombre == "admin"
    assert usuario.password == "admin123"
    assert usuario.rol == "admin"

def test_iniciar_sesion():
    usuario = Usuario(1, "admin", "admin", "admin123")
    assert usuario.iniciar_sesion("admin123") is True

def test_cambiar_contraseña():
    usuario = Usuario(1, "admin", "admin", "admin123")
    usuario.cambiar_contraseña("newpass")
    assert usuario.password == "newpass"

def test_crear_usuario_contraseña_invalida():
    usuario = Usuario(1, "admin", "admin", "")
    with pytest.raises(ContrasenaInvalidaError):
        usuario.validar()

def test_iniciar_sesion_credenciales_invalidas():
    usuario = Usuario(1, "admin", "admin", "admin123")
    with pytest.raises(CredencialesInvalidasError):
        usuario.iniciar_sesion("wrongpass")

def test_validar_expiracion():
    usuario = Usuario(1, "admin", "admin", "admin123")
    # Fecha hace más de 2 años
    with pytest.raises(ContrasenaExpiradaError):
        usuario.validar_expiracion("01/01/2020")

def test_to_dict_from_dict():
    usuario = Usuario(1, "admin", "admin", "admin123")
    d = usuario.to_dict()
    usuario2 = Usuario.from_dict(d)
    assert usuario2.id == usuario.id
    assert usuario2.nombre == usuario.nombre
    assert usuario2.rol == usuario.rol
    assert usuario2.password == usuario.password

def test_validar_contraseña_estatica():
    assert Usuario.validar_contraseña("abcd1234") is True
    assert Usuario.validar_contraseña("") is False
    assert Usuario.validar_contraseña("abc") is False

def test_nombre_usuario_invalido():
    usuario = Usuario(1, "", "admin", "admin123")
    with pytest.raises(ValueError):
        usuario.validar()

def test_nombre_usuario_corto():
    usuario = Usuario(1, "ab", "admin", "admin123")
    with pytest.raises(ValueError):
        usuario.validar()

def test_rol_no_valido():
    usuario = Usuario(1, "admin", "otro", "admin123")
    with pytest.raises(ValueError):
        usuario.validar()

def test_password_vacia():
    usuario = Usuario(1, "admin", "admin", "")
    with pytest.raises(ContrasenaInvalidaError):
        usuario.validar()

def test_password_corta():
    usuario = Usuario(1, "admin", "admin", "abc")
    with pytest.raises(ContrasenaInvalidaError):
        usuario.cambiar_contraseña("") 