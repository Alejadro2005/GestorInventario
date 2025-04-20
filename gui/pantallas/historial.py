"""
Módulo para visualizar el historial completo de ventas registradas en el sistema.

Contiene la pantalla que muestra un listado detallado de todas las transacciones comerciales realizadas.
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty


class HistorialScreen(Screen):
    """
    Pantalla que muestra el registro histórico de ventas con detalles completos.

    Attributes:
        tienda (ObjectProperty): Conexión al módulo de tienda que gestiona el historial de ventas
    """

    tienda = ObjectProperty(None)

    def on_pre_enter(self):
        """
        Actualiza la lista de ventas al entrar a la pantalla.

        Obtiene el historial de la tienda y formatea los datos para su visualización
        en el widget de lista correspondiente.
        """
        historial = self.tienda.generar_historial()
        self.ids.lista_ventas.data = [{
            'texto_venta': f"""[b]Venta #{venta['id']}[/b]
            [b]Fecha:[/b] {venta['fecha']}
            [b]Productos:[/b] {', '.join(venta['productos'])}
            [b]Total:[/b] ${venta['total']:.2f}
            [b]Empleado:[/b] {venta['empleado']}"""
        } for venta in historial]