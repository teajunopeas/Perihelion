import os
import importlib

modulos = [f[:-3] for f in os.listdir(os.path.dirname(__file__)) if f.endswith(".py") and f != "__init__.py"]
__all__ = []

for modulo in modulos:
    mod = importlib.import_module(f".{modulo}", package=__name__)
    globals()[modulo] = mod
    __all__.append(modulo)