import os
import importlib

# Obtenemos la ruta del directorio actual (donde está este __init__.py)
CURRENT_DIR = os.path.dirname(__file__)

# Listamos todos los archivos .py excepto __init__.py
module_names = [
    filename[:-3]
    for filename in os.listdir(CURRENT_DIR)
    if filename.endswith(".py") and filename != "__init__.py"
]

# Definimos __all__ para indicar qué nombres se exportan al usar 'from utils import *'
__all__ = []

# Importamos dinámicamente cada módulo y sus nombres públicos
for module_name in module_names:
    # Importar el módulo
    module = importlib.import_module(f".{module_name}", package=__name__)
    
    # Agregar el módulo como atributo del paquete (opcional)
    globals()[module_name] = module
    
    # Reexportar los nombres públicos del módulo
    for attr in dir(module):
        if not attr.startswith("_"):  # Filtrar atributos privados (que comienzan con "_")
            globals()[attr] = getattr(module, attr)
            __all__.append(attr)
