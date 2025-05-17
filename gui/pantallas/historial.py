"""
Módulo para visualizar el historial completo de ventas registradas en el sistema.

Contiene la pantalla que muestra un listado detallado de todas las transacciones comerciales realizadas.
"""

from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.metrics import dp


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
        try:
            historial = self.tienda.generar_historial()
            print("[DEBUG] Historial generado:", historial)
            # Eliminar duplicados por ID de venta
            ventas_unicas = {v['id']: v for v in historial}.values()
            
            # Ordenar ventas por ID de forma descendente (más recientes primero)
            ventas_ordenadas = sorted(ventas_unicas, key=lambda x: x['id'], reverse=True)
            
            self.ids.lista_ventas.data = [{
                'texto_venta': self._formatear_venta(venta)
            } for venta in ventas_ordenadas]
        except Exception as e:
            self.mostrar_popup("❌ Error", str(e))

    def _formatear_venta(self, venta):
        """
        Formatea los datos de una venta para su visualización.

        Args:
            venta (dict): Datos de la venta a formatear

        Returns:
            str: Texto formateado con los detalles de la venta
        """
        # Calcular el ancho máximo para los productos
        max_ancho = 60  # Ancho máximo en caracteres
        
        # Formatear cada producto para que no exceda el ancho máximo
        productos_formateados = []
        for producto in venta['productos']:
            if len(producto) > max_ancho:
                # Dividir el texto en múltiples líneas si es muy largo
                palabras = producto.split()
                linea_actual = ""
                for palabra in palabras:
                    if len(linea_actual) + len(palabra) + 1 <= max_ancho:
                        linea_actual += (palabra + " ")
                    else:
                        productos_formateados.append(f"   {linea_actual.strip()}")
                        linea_actual = palabra + " "
                if linea_actual:
                    productos_formateados.append(f"   {linea_actual.strip()}")
            else:
                productos_formateados.append(f"   {producto}")

        # Construir el texto formateado con formato de moneda
        return (
            f"[b]Venta #{venta['id']}[/b]\n"
            f"Fecha: {venta['fecha']}\n"
            f"Empleado: {venta['empleado']}\n"
            f"[b]Productos:[/b]\n" +
            "\n".join(productos_formateados) + "\n"
            f"[b]Total: ${venta['total']:,.2f}[/b]\n"
            "------------------------------"
        )

    def borrar_historial(self):
        try:
            mensaje = self.tienda.borrar_historial_ventas()
            self.on_pre_enter()  # Recargar la vista
            self.mostrar_popup("✅ Éxito", mensaje)
        except Exception as e:
            self.mostrar_popup("❌ Error", str(e))

    def mostrar_popup(self, titulo, mensaje):
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        Popup(title=titulo, content=Label(text=mensaje, color=(0, 0, 0, 1)), size_hint=(0.6, 0.4)).open()