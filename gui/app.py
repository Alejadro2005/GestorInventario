# Importaciones CORRECTAS desde los nuevos módulos:
from gui.pantallas.base_screens import MainScreen, LoginScreen
from gui.pantallas.productos import ProductosMenuScreen, AgregarProductoScreen, EliminarProductoScreen, ActualizarStockScreen, VerInventarioScreen
from gui.pantallas.usuarios import UsuariosMenuScreen, CrearUsuarioScreen, EliminarUsuarioScreen, ListarUsuariosScreen
from gui.pantallas.ventas import VentasScreen
from gui.pantallas.historial import HistorialScreen
from cli.consoleui import ConsoleUI
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

# Cargar archivos .kv (mantener igual)
kv_files = [
    'gui/kv/tienda.kv',
    'gui/pantallas/productosmenuscreen.kv',
    'gui/pantallas/agregarproductoscreen.kv',
    'gui/pantallas/inventarioscreen.kv',
    'gui/pantallas/ventasscreen.kv',
    'gui/pantallas/historialscreen.kv',
    'gui/pantallas/usuariosmenuscreen.kv',
    'gui/pantallas/crearusuarioscreen.kv',
    'gui/pantallas/listarusuarioscreen.kv',
    'gui/pantallas/eliminarusuarioscreen.kv',
    'gui/pantallas/eliminarproductoscreen.kv',
    'gui/pantallas/loginscreen.kv',
    'gui/pantallas/actualizarstockscreen.kv',
    'gui/componentes/popups.kv'
]

for kv_file in kv_files:
    Builder.load_file(kv_file)

Window.clearcolor = (1, 1, 1, 1)

class TiendaApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.console_ui = ConsoleUI()
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
             {'inventario': self.console_ui.inventario, 'console_ui': self.console_ui}),
            ('eliminar_producto', EliminarProductoScreen,
             {'inventario': self.console_ui.inventario, 'console_ui': self.console_ui}),
            ('actualizar_stock', ActualizarStockScreen,
             {'inventario': self.console_ui.inventario, 'console_ui': self.console_ui}),
            ('ver_inventario', VerInventarioScreen, {'inventario': self.console_ui.inventario}),
            ('usuarios_menu', UsuariosMenuScreen, {'gestor': self.console_ui.gestor}),
            ('crear_usuario', CrearUsuarioScreen, {'gestor': self.console_ui.gestor}),
            ('eliminar_usuario', EliminarUsuarioScreen, {'gestor': self.console_ui.gestor}),
            ('listar_usuarios', ListarUsuariosScreen, {'gestor': self.console_ui.gestor}),
            ('ventas', VentasScreen, {'inventario': self.console_ui.inventario, 'tienda': self.console_ui.tienda,
                                      'console_ui': self.console_ui}),
            ('historial', HistorialScreen, {'tienda': self.console_ui.tienda}),
        ]
        for nombre, clase, *args in pantallas:
            pantalla = clase(name=nombre)
            if args:
                for prop, valor in args[0].items():
                    setattr(pantalla, prop, valor)
            self.sm.add_widget(pantalla)
if __name__ == '__main__':
    TiendaApp().run()