import json
import os
import numpy as np
from core.company import Company
from utils import helpers

DEFAULT_FILENAME = "partida.json"

def validate_filename(filename: str) -> str:
    """
    Valida que el nombre del archivo tenga una extensión .json.
    Si no tiene extensión, agrega .json.
    """
    if not filename.endswith(".json"):
        filename += ".json"
    return filename

def save_game(simulation, filename: str = DEFAULT_FILENAME) -> bool:
    """
    Guarda el estado de la simulación en un archivo JSON.

    Args:
        simulation: Instancia de la clase Simulation.
        filename: Nombre del archivo donde se guardará la partida (default: partida.json).

    Returns:
        bool: True si se guardó correctamente, False si hubo un error.
    """
    try:
        filename = validate_filename(filename)
        # Preparar datos de las empresas
        companies_data = [
            {
                "nombre": company.nombre,
                "presupuesto": company.presupuesto,
                "pvp": company.pvp,
                "coste_fijo": company.coste_fijo,
                "coste_variable": company.coste_variable,
                "stock": company.stock,
                "coste_almacenamiento_unitario": company.coste_almacenamiento_unitario,
                "coste_ruptura_unitario": company.coste_ruptura_unitario,
                "coste_no_servicio_unitario": company.coste_no_servicio_unitario,
                "ventas_reales_mes": company.ventas_reales_mes,
                # TODO: Agregar otros atributos de Company si son necesarios (e.g., inversiones históricas)
            }
            for company in simulation.companies
        ]
        
        # Preparar datos de la simulación
        sim_data = {
            "month": simulation.current_month,
            "markov_matrix": simulation.markov_matrix.tolist(),  # Convertir NumPy a lista
            "ruptadm_global": simulation.ruptadm_global,
            "companies": companies_data,
            # TODO: Incluir demanda total o datos históricos si se gestionan en Simulation
        }
        
        # Guardar en archivo
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(sim_data, f, indent=4)
        print(f"Partida guardada exitosamente en {filename}")
        return True
    
    except Exception as e:
        print(f"Error al guardar la partida: {str(e)}")
        return False

def load_game(filename: str = DEFAULT_FILENAME) -> dict:
    """
    Carga una partida desde un archivo JSON y devuelve los datos para restaurar la simulación.

    Args:
        filename: Nombre del archivo a cargar (default: partida.json).

    Returns:
        dict: Diccionario con los datos de la simulación, o None si hay un error.
    """
    try:
        filename = validate_filename(filename)
        if not os.path.exists(filename):
            print(f"El archivo {filename} no existe.")
            return None
        
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Validar datos básicos
        required_keys = ["month", "markov_matrix", "ruptadm_global", "companies"]
        if not all(key in data for key in required_keys):
            print("El archivo JSON no contiene todos los datos necesarios.")
            return None
        
        # Convertir markov_matrix a NumPy
        data["markov_matrix"] = np.array(data["markov_matrix"])
        
        # Validar número de empresas
        if len(data["companies"]) != 4:  # Asumiendo 4 empresas
            print("El archivo debe contener datos de exactamente 4 empresas.")
            return None
        
        # Validar atributos de empresas
        required_company_keys = [
            "nombre", "presupuesto", "pvp", "coste_fijo", "coste_variable",
            "stock", "coste_almacenamiento_unitario", "coste_ruptura_unitario",
            "coste_no_servicio_unitario", "ventas_reales_mes"
        ]
        for company_data in data["companies"]:
            if not all(key in company_data for key in required_company_keys):
                print("Datos de empresa incompletos en el archivo.")
                return None
        
        print(f"Partida cargada exitosamente desde {filename}")
        return data
    
    except Exception as e:
        print(f"Error al cargar la partida: {str(e)}")
        return None

def prompt_filename() -> str:
    """
    Solicita al usuario el nombre del archivo, con opción de usar el nombre por defecto.

    Returns:
        str: Nombre del archivo elegido.
    """
    print("¿Qué nombre desea darle al fichero?")
    print("1) Escriba 1 para elegir el nombre por defecto (partida.json).")
    print("2) Escriba 2 para poner otro nombre.")
    
    choice = helpers.Unodos()
    
    if choice == "1":
        return DEFAULT_FILENAME
    else:
        filename = input("Escriba el nombre del fichero: ")
        return validate_filename(filename)

# TODO: Implementar función para validar integridad de datos (e.g., matriz de Markov estocástica)
# def validate_data(data: dict) -> bool:
#     """
#     Valida que los datos cargados sean consistentes (e.g., matriz de Markov suma 1 por columna).
#     """
#     pass