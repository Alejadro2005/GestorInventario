import logging
import os
from datetime import datetime

def setup_logger():
    """
    Configura el sistema de logging para la aplicación GestorInventario.
    - Crea un directorio 'logs' si no existe.
    - Configura el logger global con formato estándar.
    - Agrega handlers para archivo y consola.
    
    Returns:
        logging.Logger: Instancia configurada del logger.
    """
    # Crear directorio de logs si no existe
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Configurar el logger
    logger = logging.getLogger('GestorInventario')
    logger.setLevel(logging.INFO)

    # Formato del log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Handler para archivo (guarda logs diarios)
    log_file = f'logs/gestor_inventario_{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler para consola (muestra logs en tiempo real)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

# Instancia global del logger para ser usada en toda la aplicación
logger = setup_logger() 