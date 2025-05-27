from modelos.inventario import Inventario
from modulos.gestor_usuarios import GestorUsuarios
from modulos.tienda import Tienda
from modelos.usuario import Usuario
from utils.logger import logger

class ConsoleUI:
    """
    Clase que maneja la interfaz de consola y la integración con la interfaz gráfica.
    
    Attributes:
        inventario (Inventario): Instancia del inventario
        gestor (GestorUsuarios): Instancia del gestor de usuarios
        tienda (Tienda): Instancia de la tienda
        usuario_actual (Usuario): Usuario actualmente autenticado
    """
    
    def __init__(self, inventario: Inventario, gestor: GestorUsuarios):
        """
        Inicializa la interfaz de consola.
        
        Args:
            inventario (Inventario): Instancia del inventario
            gestor (GestorUsuarios): Instancia del gestor de usuarios
        """
        self.inventario = inventario
        self.gestor = gestor
        self.tienda = Tienda(inventario.db, inventario)
        self.usuario_actual = None
        logger.info("ConsoleUI inicializada correctamente")

    def autenticar_usuario(self, id_usuario: int, password: str) -> bool:
        """
        Autentica un usuario en el sistema.
        
        Args:
            id_usuario (int): ID del usuario
            password (str): Contraseña del usuario
            
        Returns:
            bool: True si la autenticación fue exitosa
            
        Raises:
            ValueError: Si las credenciales son inválidas
        """
        try:
            usuario = self.gestor.obtener_usuario(id_usuario)
            if not usuario:
                raise ValueError("Usuario no encontrado")
                
            if usuario.rol != "admin":
                raise ValueError("Solo usuarios con rol ADMIN pueden ingresar")
                
            usuario.iniciar_sesion(password)
            self.usuario_actual = usuario
            logger.info(f"Usuario {usuario.nombre} autenticado correctamente")
            return True
            
        except Exception as e:
            logger.error(f"Error en autenticación: {str(e)}")
            raise ValueError("Credenciales inválidas")

    def cerrar_sesion(self):
        """Cierra la sesión del usuario actual."""
        if self.usuario_actual:
            logger.info(f"Usuario {self.usuario_actual.nombre} cerró sesión")
            self.usuario_actual = None 