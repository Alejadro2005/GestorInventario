# Importaciones CORRECTAS desde los nuevos módulos:
from gui.pantallas.base_screens import MainScreen, LoginScreen
from gui.pantallas.productos import ProductosMenuScreen, AgregarProductoScreen, EliminarProductoScreen, ActualizarStockScreen, VerInventarioScreen
from gui.pantallas.usuarios import UsuariosMenuScreen, CrearUsuarioScreen, EliminarUsuarioScreen, ListarUsuariosScreen
from gui.pantallas.ventas import VentasScreen
from gui.pantallas.historial import HistorialScreen
from src.modulos.console_ui import ConsoleUI
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from src.database.postgres_database import PostgresDatabase
from src.modelos.inventario import Inventario
from src.modulos.gestor_usuarios import GestorUsuarios
import os
from src.utils.logger import logger

# Obtener la ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cargar archivos .kv con rutas absolutas
kv_files = [
    os.path.join(BASE_DIR, 'gui/pantallas/mainscreen.kv'),
    os.path.join(BASE_DIR, 'gui/pantallas/productosmenuscreen.kv'),
    os.path.join(BASE_DIR, 'gui/pantallas/agregarproductoscreen.kv'),
    os.path.join(BASE_DIR, 'gui/pantallas/inventarioscreen.kv'),
    os.path.join(BASE_DIR, 'gui/pantallas/ventasscreen.kv'),
    os.path.join(BASE_DIR, 'gui/pantallas/historialscreen.kv'),
    os.path.join(BASE_DIR, 'gui/pantallas/usuariosmenuscreen.kv'),
    os.path.join(BASE_DIR, 'gui/pantallas/crearusuarioscreen.kv'),
    os.path.join(BASE_DIR, 'gui/pantallas/listarusuarioscreen.kv'),
    os.path.join(BASE_DIR, 'gui/pantallas/eliminarusuarioscreen.kv'),
    os.path.join(BASE_DIR, 'gui/pantallas/eliminarproductoscreen.kv'),
    os.path.join(BASE_DIR, 'gui/pantallas/loginscreen.kv'),
    os.path.join(BASE_DIR, 'gui/pantallas/actualizarstockscreen.kv')
]

for kv_file in kv_files:
    if os.path.exists(kv_file):
        Builder.load_file(kv_file)
    else:
        logger.warning(f"Archivo .kv no encontrado: {kv_file}")

Window.clearcolor = (1, 1, 1, 1)

class TiendaApp(App):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.inventario = Inventario(self.db)
        self.gestor_usuarios = GestorUsuarios(self.db)
        self.console_ui = ConsoleUI(self.inventario, self.gestor_usuarios)
        self.sm = ScreenManager()

    def build(self):
        self._configurar_pantallas()
        return self.sm

    def _configurar_pantallas(self):
        pantallas = [
            ('main', MainScreen),
            ('login', LoginScreen, {'console_ui': self.console_ui}),
            ('productos_menu', ProductosMenuScreen, {'console_ui': self.console_ui}),
            ('agregar_producto', AgregarProductoScreen, 
             {'inventario': self.inventario, 'console_ui': self.console_ui}),
            ('eliminar_producto', EliminarProductoScreen,
             {'inventario': self.inventario, 'console_ui': self.console_ui}),
            ('actualizar_stock', ActualizarStockScreen,
             {'inventario': self.inventario, 'console_ui': self.console_ui}),
            ('ver_inventario', VerInventarioScreen, {'inventario': self.inventario}),
            ('usuarios_menu', UsuariosMenuScreen, {'gestor': self.gestor_usuarios, 'console_ui': self.console_ui}),
            ('crear_usuario', CrearUsuarioScreen, {'gestor': self.gestor_usuarios, 'console_ui': self.console_ui}),
            ('eliminar_usuario', EliminarUsuarioScreen, {'gestor': self.gestor_usuarios, 'console_ui': self.console_ui}),
            ('listar_usuarios', ListarUsuariosScreen, {'gestor': self.gestor_usuarios, 'console_ui': self.console_ui}),
            ('ventas', VentasScreen, {'inventario': self.inventario, 'tienda': self.console_ui.tienda,
                                     'console_ui': self.console_ui}),
            ('historial', HistorialScreen, {'tienda': self.console_ui.tienda}),
        ]
        for nombre, clase, *args in pantallas:
            pantalla = clase(name=nombre)
            if args:
                for prop, valor in args[0].items():
                    setattr(pantalla, prop, valor)
            self.sm.add_widget(pantalla)
        self.sm.current = 'main'  # Cambiar a pantalla principal

if __name__ == '__main__':
    TiendaApp().run()