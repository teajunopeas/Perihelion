import subprocess
import os

# Ruta al intérprete de Python del entorno virtual
python_path = r"c:\Users\elian\OneDrive - Universidad de Las Palmas de Gran Canaria\Curso 24-25 2do semestre\MNF\Perihelion\venv\Scripts\python.exe"

# Ruta al archivo principal
script_path = r"Proyecto sara\juego4empresas.py"

# Obtener la ruta absoluta del script
script_full_path = os.path.abspath(script_path)

# Directorio donde se encuentra el script
script_dir = os.path.dirname(script_full_path)

# Ejecutar el script principal
with open("Ejecucion.txt", "w", encoding="utf-8") as f:
    subprocess.run(
        [python_path, script_full_path],
        stdout=f,
        stderr=subprocess.STDOUT,
        cwd=script_dir  # Cambiar al directorio del script
    )