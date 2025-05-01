# Importaciones
from utils import *
from core import *
from utils import *
import numpy as np

# Constantes y configuración inicial
NUM_EMPRESAS = 4  # Número de empresas
MESES_SIMULACION = 12  # Número de meses de simulación
DEMANDA_TOTAL_MES = 10000  # Demanda total mensual (ejemplo)

# Valores iniciales para las empresas (ejemplo genérico)
INITIAL_BUDGET = 1000000
INITIAL_PVP = 10000
INITIAL_FIXED_COST = 50000
INITIAL_VARIABLE_COST = 8000
INITIAL_STOCK = 100
INITIAL_DEMAND = 10000
STORAGE_COST_PER_UNIT = 100
STOCKOUT_COST_PER_UNIT = 2000
NO_SERVICE_COST_PER_UNIT = 1000
RUPTADM_GLOBAL = 1  # 1: Clientes esperan; 2: Clientes no esperan

# TODO: Implementar opciones para pedir los valores o e otro caso, cargarlos de algun archivo almacenado en data
def get_initial_config():
    """Solicita al usuario los valores iniciales para la simulación."""
    print("\n=== Configuración Inicial ===")
    opciones = ["Cargar partida guardada", "Iniciar nueva simulación"]
    return Unodos(opciones=opciones) # type: ignore

def create_new_simulation():
    """Crea una nueva simulación con valores predeterminados."""
    companies = []
    for i in range(NUM_EMPRESAS):
        config = {
            'nombre': f'Empresa {i+1}',
            'presupuesto_inicial': INITIAL_BUDGET,
            'pvp_inicial': INITIAL_PVP,
            'coste_fijo_mensual': INITIAL_FIXED_COST,
            'coste_variable_unitario': INITIAL_VARIABLE_COST,
            'stock_inicial': INITIAL_STOCK,
            'coste_almacenamiento_unitario': STORAGE_COST_PER_UNIT,
            'coste_ruptura_unitario': STOCKOUT_COST_PER_UNIT,
            'coste_no_servicio_unitario': NO_SERVICE_COST_PER_UNIT,
        }
        company = Company(config, RUPTADM_GLOBAL) # type: ignore
        companies.append(company)

    initial_markov = np.full((NUM_EMPRESAS, NUM_EMPRESAS), 1 / NUM_EMPRESAS)
    return Simulation(companies, initial_markov, INITIAL_DEMAND, RUPTADM_GLOBAL) # type: ignore

def main():
    # TODO: Si tienes datos históricos específicos (como en el PDF), carga o define los valores iniciales aquí.
    # Por ahora, usamos valores genéricos.
    
    # Limpiar la consola
    clear_console() # type: ignore como se importa desde __init__.py, no es necesario importar helpers.clear_console() de nuevo
    print("Iniciando la simulación de empresas...")

    # Elegir entre cargar una partida guardada o iniciar una nueva simulación
    choice = get_initial_config()
    sim = None
    if choice == 1:
       filename = promt_filename() # type: ignore
       sim = Simulation.load_state(filename) # type: ignore
       if sim is None:
           print("Error al cargar la partida guardada. Iniciando nueva simulación.")
           sim = create_new_simulation()
    else:
        # Crear una nueva simulación
        sim = create_new_simulation()

    if sim is None:
        print("Error al crear la simulación.")
        return 1

    # Crear las empresas
    companies = []
    for i in range(NUM_EMPRESAS):
        config = {
            'nombre': f'Empresa {i+1}',
            'presupuesto_inicial': INITIAL_BUDGET,
            'pvp_inicial': INITIAL_PVP,
            'coste_fijo_mensual': INITIAL_FIXED_COST,
            'coste_variable_unitario': INITIAL_VARIABLE_COST,
            'stock_inicial': INITIAL_STOCK,
            'coste_almacenamiento_unitario': STORAGE_COST_PER_UNIT,
            'coste_ruptura_unitario': STOCKOUT_COST_PER_UNIT,
            'coste_no_servicio_unitario': NO_SERVICE_COST_PER_UNIT,
        }
        company = Company(config, RUPTADM_GLOBAL) # type: ignore
        companies.append(company)

    # Matriz de Markov inicial (todos los valores iguales a 0.25)
    initial_markov = np.full((NUM_EMPRESAS, NUM_EMPRESAS), 1 / NUM_EMPRESAS)

    # Inicializar la simulación
    sim = Simulation(companies, initial_markov, RUPTADM_GLOBAL, INITIAL_DEMAND) # type: ignore


    sim.run_simulation(MESES_SIMULACION)  # Ejecutar la simulación completa (se omite en este caso porque no esta implementada la demanda total)

    # Ejecutar la simulación por cada mes
    for month in range(MESES_SIMULACION):
        print(f"--- Mes {month+1} ---")
        
        # TODO: Si necesitas establecer estrategias específicas para las empresas antes de cada mes,
        # puedes hacerlo aquí. Por ejemplo:
        # for company in companies:
        #     company.decidir_estrategias(nuevo_pvp=..., inv_mkt=..., inv_tech=...)
        
        

        # Ejecutar un paso de la simulación
        # sim.run_step()  # Pasar la demanda total del mes (Se omite en este caso porque no esta implementada la demanda total)
        
        # Imprimir resultados del mes (opcional)
        for company in companies:
            print(f"{company.nombre}: Ventas = {company.ventas_reales_mes}, Presupuesto = {company.presupuesto}")
            

    # Imprimir resultados finales (opcional)
    print("\n--- Resultados finales ---")
    for company in companies:
        print(f"{company.nombre}: Presupuesto final = {company.presupuesto}")

    try:
        sim.save_state("partida_final.json")
    except RuntimeError as e:
        print(f"Error al guardar la partida final: {e}")

    return 0

if __name__ == "__main__":
    main()