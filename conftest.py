import os
import sys

# Obtener la ruta absoluta del directorio raíz
root_dir = os.path.abspath(os.path.dirname(__file__))
src_dir = os.path.join(root_dir, 'src')

# Agregar solo el directorio raíz al PYTHONPATH
sys.path.insert(0, root_dir)

# Agregar tanto el directorio raíz como src al PYTHONPATH
sys.path.insert(0, src_dir) 