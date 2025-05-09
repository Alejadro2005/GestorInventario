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
from src.database.sqlite_database import SQLiteDatabase

@pytest.fixture
def db():
    """Fixture que proporciona una instancia de base de datos para las pruebas."""
    db = SQLiteDatabase(":memory:")
    db.connect()
    db.create_tables()
    yield db
    db.disconnect()

@pytest.fixture
def gestor(db):
    """Fixture que proporciona una instancia de GestorUsuarios para las pruebas."""
    return GestorUsuarios(db)

def test_crear_usuario(gestor):
    """
    Test para verificar que se puede crear un usuario correctamente.

    Se crea un usuario con un ID único y se comprueba que el mensaje de retorno
    indique éxito.

    Asserts:
        str: El mensaje esperado de confirmación de creación del usuario.
    """
    usuario = Usuario(1, "usuario_nuevo", "admin", "contraseña")  # ID único
    mensaje_esperado = "Usuario 'usuario_nuevo' creado con éxito."
    assert gestor.crear_usuario(usuario) == mensaje_esperado


def test_usuario_validar_rol(gestor):
    """
    Test para verificar que el rol de un usuario se valide correctamente.

    Se crea un usuario y luego se comprueba que el método `validar_rol` retorne True
    cuando el rol es el correcto.

    Asserts:
        bool: True si el rol del usuario coincide con el proporcionado.
    """
    usuario = Usuario(1000, "jose", "empleado", "1234")  # ID único
    gestor.crear_usuario(usuario)
    assert gestor.validar_rol(1000, "empleado") == True


def test_eliminar_usuario3(gestor):
    """
    Test para verificar que se pueda eliminar un usuario correctamente.

    Se crean tres usuarios, se elimina uno de ellos y se comprueba que el mensaje
    de eliminación sea el esperado.

    Asserts:
        str: El mensaje esperado de confirmación de eliminación del usuario.
    """
    usuario = Usuario(1, "jose", "empleado", "1234")
    usuario2 = Usuario(2, "alejandro", "empleado", "4321")
    usuario3 = Usuario(3, "pepe", "empleado", "9876")
    gestor.crear_usuario(usuario)
    gestor.crear_usuario(usuario2)
    gestor.crear_usuario(usuario3)
    assert gestor.eliminar_usuario(3) == "Usuario 'pepe' eliminado con éxito."


def test_iniciar_sesion():
    """
    Test para verificar que un usuario pueda iniciar sesión con la contraseña correcta.

    Se crea un usuario y se intenta iniciar sesión con la contraseña correspondiente.

    Asserts:
        bool: True si la contraseña es correcta.
    """
    usuario = Usuario(1, "jose", "empleado", "1234")
    assert usuario.iniciar_sesion("1234") == True


def test_cambiar_contraseña():
    """
    Test para verificar que un usuario pueda cambiar su contraseña correctamente.

    Se cambia la contraseña del usuario y se comprueba que el nuevo valor sea retornado.

    Asserts:
        str: La nueva contraseña asignada.
    """
    usuario = Usuario(1, "jose", "empleado", "1234")
    assert usuario.cambiar_contraseña("4321") == "4321"


def test_iniciar_sesion2():
    """
    Test duplicado para verificar que un usuario pueda iniciar sesión con la contraseña correcta.

    Se utiliza la misma lógica que `test_iniciar_sesion` para validar comportamiento repetido.

    Asserts:
        bool: True si la contraseña es correcta.
    """
    usuario = Usuario(1, "jose", "empleado", "1234")
    assert usuario.iniciar_sesion("1234") == True


# Tests Error
def test_crear_usuario_duplicado(gestor):
    """
    Test para verificar que no se permita crear un usuario con un ID duplicado.

    Se intenta crear un usuario que ya fue registrado previamente, lo que debe
    generar una excepción `UsuarioDuplicadoError`.

    Raises:
        UsuarioDuplicadoError: Si se intenta registrar un usuario con un ID existente.
    """
    usuario = Usuario(1, "jose", "empleado", "1234")
    gestor.crear_usuario(usuario)

    with pytest.raises(UsuarioDuplicadoError, match="El usuario con ID 1 ya existe"):
        gestor.crear_usuario(usuario)


def test_validar_rol_usuario_no_existente(gestor):
    """
    Test para verificar que se lanza una excepción al validar el rol de un usuario inexistente.

    Raises:
        UsuarioNoEncontradoError: Si se intenta validar el rol de un usuario no registrado.
    """
    with pytest.raises(UsuarioNoEncontradoError, match="El usuario con ID 99 no existe"):
        gestor.validar_rol(99, "empleado")


def test_eliminar_usuario_inexistente(gestor):
    """
    Test para verificar que se lanza una excepción al intentar eliminar un usuario inexistente.

    Raises:
        UsuarioNoEncontradoError: Si se intenta eliminar un usuario no registrado.
    """
    with pytest.raises(UsuarioNoEncontradoError, match="El usuario con ID 99 no existe"):
        gestor.eliminar_usuario(99)


def test_crear_usuario_contraseña_invalida():
    """
    Test para verificar que no se permite crear un usuario con contraseña inválida.

    Se intenta crear un usuario con una contraseña vacía, lo que debe generar una
    excepción `ContraseñaInvalidaError`.

    Raises:
        ContraseñaInvalidaError: Si la contraseña no cumple con los requisitos mínimos.
    """
    with pytest.raises(ContraseñaInvalidaError, match="La contraseña no cumple con los requisitos mínimos"):
        Usuario(1, "jose", "empleado", "")


def test_iniciar_sesion_fallida():
    """
    Test para verificar que iniciar sesión con una contraseña incorrecta lanza un error.

    Se crea un usuario y se intenta iniciar sesión con una contraseña errónea.

    Raises:
        CredencialesInvalidasError: Si las credenciales no son válidas.
    """
    usuario = Usuario(1, "jose", "empleado", "1234")

    with pytest.raises(CredencialesInvalidasError, match="Credenciales incorrectas"):
        usuario.iniciar_sesion("0000")


def test_cambiar_contraseña_invalida():
    """
    Test para verificar que no se permita cambiar la contraseña a un valor inválido.

    Se intenta cambiar la contraseña a una vacía, lo que debe generar una excepción.

    Raises:
        ContraseñaInvalidaError: Si la nueva contraseña no cumple con los requisitos mínimos.
    """
    usuario = Usuario(1, "jose", "empleado", "1234")

    with pytest.raises(ContraseñaInvalidaError, match="La contraseña no cumple con los requisitos mínimos"):
        usuario.cambiar_contraseña("")



# Test caso extremo
def test_rol_con_emojis():
    """
    Test para verificar que no se aceptan roles con caracteres no válidos como emojis.

    Raises:
        RolInvalidoError: Si el rol contiene caracteres inválidos.
    """
    with pytest.raises(RolInvalidoError):
        Usuario(8, "Ana", "admin🔥", "Pass1234")


def test_nombre_usuario_largo():
    """
    Test para verificar que no se permita un nombre de usuario excesivamente largo.

    Raises:
        NombreUsuarioInvalidoError: Si el nombre de usuario excede el límite permitido.
    """
    with pytest.raises(NombreUsuarioInvalidoError):
        Usuario(9, "A" * 100, "empleado", "SecurePass1")


def test_contraseña_expirada():
    """
    Test para verificar que se detecta una contraseña expirada.

    Se simula una contraseña con fecha de expiración pasada.

    Raises:
        ContraseñaExpiradaError: Si la contraseña ha expirado.
    """
    usuario = Usuario(1, "jose", "empleado", "1234")
    with pytest.raises(ContraseñaExpiradaError):
        usuario.validar_expiracion("01/01/2020")


def test_crear_usuario_sin_nombre():
    """
    Test para verificar que no se permite crear un usuario sin nombre.

    Raises:
        NombreUsuarioInvalidoError: Si el nombre de usuario está vacío.
    """
    with pytest.raises(NombreUsuarioInvalidoError, match="El nombre de usuario no puede estar vacío"):
        Usuario(10, "", "empleado", "Pass1234")


def test_crear_usuario_con_rol_inexistente():
    """
    Test para verificar que no se permite asignar un rol que no está definido en el sistema.

    Raises:
        RolInvalidoError: Si el rol especificado no es válido.
    """
    with pytest.raises(RolInvalidoError, match="El rol 'superheroe' no es válido"):
        Usuario(11, "carlos", "superheroe", "Pass1234")


def test_validar_rol_usuario_eliminado(gestor):
    """
    Test para verificar que se lanza una excepción al validar el rol de un usuario eliminado.

    Raises:
        UsuarioNoEncontradoError: Si se intenta validar el rol de un usuario eliminado.
    """
    usuario = Usuario(1, "jose", "empleado", "1234")
    gestor.crear_usuario(usuario)
    gestor.eliminar_usuario(1)

    with pytest.raises(UsuarioNoEncontradoError, match="El usuario con ID 1 no existe"):
        gestor.validar_rol(1, "empleado")
