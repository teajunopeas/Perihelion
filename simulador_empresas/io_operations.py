def load_old_game(filename='Partida.dta'):
    """
    Función para cargar datos de una partida antigua desde un fichero.
    Se simula la lectura y se retorna un diccionario con las variables necesarias.
    """
    print("Cargando partida antigua...")
    try:
        with open(filename, 'r') as f:
            data = f.readlines()
        
        # Aquí se debe parsear 'data' para extraer las variables.
        # Para efectos del ejemplo se retornan valores de ejemplo.
        return {
            'UD': np.array([[10], [10], [10], [10]]),
            'V': np.array([[20], [20], [20], [20]]),
            'Ventasreales': np.array([[20], [20], [20], [20]]),
            'VENTASPENDIENTES': np.array([[0], [0], [0], [0]]),
            'PVP': np.array([[100.0], [100.0], [100.0], [100.0]]),
            'CF': np.array([[50], [50], [50], [50]]),
            'CV': np.array([[10.0], [10.0], [10.0], [10.0]]),
            'STOCK': np.array([[5], [5], [5], [5]]),
            'CALM': np.array([[2], [2], [2], [2]]),
            'CNOSERV': np.array([[1], [1], [1], [1]]),
            'CRUPT': np.array([[1], [1], [1], [1]]),
            'INGRESOS': np.array([[200.0], [200.0], [200.0], [200.0]]),
            'CTOTAL': np.array([[60.0], [60.0], [60.0], [60.0]]),
            'PRESUPUESTO': np.array([[1000.0], [1000.0], [1000.0], [1000.0]]),
            'CM': np.array([[0.25, 0.25, 0.25, 0.25]]*4),
            'Calm': np.array([[2.0], [2.0], [2.0], [2.0]]),
            'ruptadm': 2,
            'Crupt': np.array([[1.0], [1.0], [1.0], [1.0]]),
            'Cnoserv': np.array([[1.0], [1.0], [1.0], [1.0]]),
            'duracion': 12  # Ejemplo
        }
    except FileNotFoundError:
        print("El fichero no existe. Asegúrese de que el nombre es correcto.")
        return None

def save_game(data, filename='Partida.dta'):
    """
    Función para guardar la partida en un fichero.
    Se guarda una versión simplificada de los datos.
    """
    print("Guardando la partida...")
    with open(filename, 'w') as f:
        for key, value in data.items():
            f.write(f"{key}: {value}\n")
    print("Partida guardada exitosamente.")