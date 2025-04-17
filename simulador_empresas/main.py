"""
Este script, simula un juego de 4 empresas que compiten en un mercado estable por ver quien consigue
llevarse más porción del mercado, esn este caso, se ambienta en la a
"""

import numpy as np
import matplotlib.pyplot as plt
import random

# Funciones auxiliares para validar la entrada del usuario

def unodos(prompt=""):
    """Solicita al usuario ingresar 1 o 2."""
    while True:
        try:
            valor = int(input(prompt))
            if valor in [1, 2]:
                return valor
            else:
                print("Por favor, ingrese 1 o 2.")
        except ValueError:
            print("Entrada no válida. Ingrese 1 o 2.")

def enteropos(prompt=""):
    """Solicita al usuario un entero positivo."""
    while True:
        try:
            valor = input(prompt)
            entero = valor%1
            if valor > 0 and entero != 0:
                return valor
            else:
                print("El valor debe ser un entero positivo.")
        except ValueError:
            print("Entrada no válida. Ingrese un entero positivo.")

def positiva(prompt=""):
    """Solicita al usuario un número (float) mayor que 0."""
    while True:
        try:
            valor = float(input(prompt))
            if valor > 0:
                return valor
            else:
                print("El valor debe ser mayor que 0.")
        except ValueError:
            print("Entrada no válida. Ingrese un número positivo.")

# Funciones 'stub' para las subrutinas personalizadas del código MATLAB

def precio_vp(PVP, CM, empresa, i, j, pvpini):
    """
    Función para modificar el precio de venta (PrecioVP).
    Aquí se solicita un nuevo precio y se actualiza la matriz.
    """
    nuevo_precio = positiva(f"Ingrese nuevo precio para {empresa[i]} en el mes {j}: ")
    PVP[i, j] = nuevo_precio
    # Se podría actualizar la matriz de Markov (CM) según alguna regla
    return PVP, CM

def marketing(i, j, CM, CTOTAL, PRESUPUESTO, empresa, PUB, duracion):
    """
    Función para invertir en marketing.
    Se solicita una inversión y se actualizan los costes totales.
    """
    inversion = positiva(f"Ingrese inversión en marketing para {empresa[i]} en el mes {j}: ")
    PUB[i, j] = inversion
    CTOTAL[i, j] += inversion
    # Se puede actualizar la matriz de Markov de forma ficticia (stub)
    return CTOTAL, CM, PUB

def mejoras(i, j, CV, CTOTAL, PRESUPUESTO, empresa, CM, mejoras_arr, duracion):
    """
    Función para invertir en mejoras tecnológicas.
    Se solicita una inversión y se actualiza el coste variable (CV) y los costes totales.
    """
    if PRESUPUESTO[i,j] <= 0:
        print('Si la empresa no tiene capital disponible, no se permite invertir en Mejoras Tecnológicas\n')
    else:
        fprintf('¿Desea modificar la inversión en Mejoras Tecnológicas del mes pasado?')
        fprintf('\n1) Teclee un 1 si desea modificarla.')
        fprintf('\n2) Teclee un 2 si no desea modificarla.\n')
        modificacion= Unodos(); #Comprobamos si es 1 ó 2

    if modificacion == 1:
        print('Placeholder')
    
    
    inversion = positiva(f"Ingrese inversión en mejoras tecnológicas para {empresa[i]} en el mes {j}: ")
    mejoras_arr[i, j] = inversion
    CTOTAL[i, j] += inversion
    # Por ejemplo, se podría reducir el coste variable en función de la inversión
    CV[i, j] = max(CV[i, j] - 0.1*inversion, 0.1)
    return CTOTAL, CV, CM, mejoras_arr

def negativo(V, j, indices):
    """
    Función para corregir ventas negativas.
    Se distribuye el 'exceso' de forma equitativa entre las demás empresas.
    """
    for idx in indices:
        exceso = -V[idx, j]
        V[idx, j] = 0
        otros = [k for k in range(len(V[:, j])) if k != idx]
        reparto = exceso // len(otros) if otros else 0
        for k in otros:
            V[k, j] += reparto
    return V

def diagrama(cme):
    """
    Stub para función de diagrama.
    En Python, plt.pie ya genera el gráfico, por lo que se puede personalizar aquí.
    """
    pass

def resultados(V, CM, duracion, UD, PRESUPUESTO, CV):
    """Función para mostrar los resultados finales de la simulación."""
    print("\nResultados finales:")
    print("Ventas finales por empresa:", V[:, -1])
    print("Presupuestos finales:", PRESUPUESTO[:, -1])
    # Se pueden agregar más detalles según se necesite.

# Función para cargar una partida antigua

def load_old_game():
    """
    Función para cargar datos de una partida antigua desde un fichero.
    Se simula la lectura y se retorna un diccionario con las variables necesarias.
    """
    print("Cargando partida antigua...")
    print("¿Qué nombre tiene el fichero de entrada?")
    print("1) Escriba 1 si tiene el nombre por defecto (Partida.dta).")
    print("2) Escriba 2 si tiene otro nombre.")
    nombrec = unodos()
    if nombrec == 1:
        filename = 'Partida.dta'
    else:
        filename = input("Escriba el nombre del fichero: ")
    # Intentar abrir el fichero
    while True:
        try:
            with open(filename, 'r') as f:
                data = f.read()
            break
        except FileNotFoundError:
            print("El fichero no existe. Escriba el nombre de un fichero válido.")
            filename = input("Nombre del fichero: ")
    # Aquí habría que parsear 'data' para extraer las variables.
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

def save_game(UD, V, Ventasreales, VENTASPENDIENTES, PVP, CF, CV, STOCK, CALM, CNOSERV, CRUPT, INGRESOS, CTOTAL, PRESUPUESTO, CM, Calm, ruptadm, Crupt, Cnoserv, j):
    """
    Función para guardar la partida en un fichero.
    Se guarda una versión simplificada de los datos.
    """
    print("Guardando la partida...")
    print("¿Qué nombre desea darle al fichero?")
    print("1) Escriba 1 para elegir el nombre por defecto (Partida.dta).")
    print("2) Escriba 2 para poner otro nombre.")
    nombre = unodos()
    if nombre == 1:
        filename = 'Partida.dta'
    else:
        filename = input("Escriba el nombre del fichero: ")
    with open(filename, 'w') as f:
        f.write(f"{UD[0, j]} {UD[1, j]} {UD[2, j]} {UD[3, j]}\n")
        f.write(f"{V[0, j]} {V[1, j]} {V[2, j]} {V[3, j]}\n")
        f.write(f"{Ventasreales[0, j]} {Ventasreales[1, j]} {Ventasreales[2, j]} {Ventasreales[3, j]}\n")
        f.write(f"{VENTASPENDIENTES[0, j]} {VENTASPENDIENTES[1, j]} {VENTASPENDIENTES[2, j]} {VENTASPENDIENTES[3, j]}\n")
        f.write(f"{PVP[0, j]} {PVP[1, j]} {PVP[2, j]} {PVP[3, j]}\n")
        # Se pueden escribir más datos según se requiera.
        for row in CM:
            f.write(" ".join(map(str, row)) + "\n")
    print("Partida guardada exitosamente.")




# Función principal que orquesta la simulación

def main():
    # Cabecera del Programa
    print("\nJuego de empresas para cuatro participantes\n")
    print("¿Desea cargar una partida anterior o empezar otra?")
    print("1) Escriba 1 para cargar una partida antigua.")
    print("2) Escriba 2 para comenzar una partida nueva.")
    cargar = unodos()
    
    Empresa = ["Mercedes", "Peugeot", "Penhard-Levassor", "Mors"]
    
    if cargar == 1:
        # Cargar partida antigua
        game_data = load_old_game()
        UD = game_data['UD']
        V = game_data['V']
        Ventasreales = game_data['Ventasreales']
        VENTASPENDIENTES = game_data['VENTASPENDIENTES']
        PVP = game_data['PVP']
        CF = game_data['CF']
        CV = game_data['CV']
        STOCK = game_data['STOCK']
        CALM = game_data['CALM']
        CNOSERV = game_data['CNOSERV']
        CRUPT = game_data['CRUPT']
        INGRESOS = game_data['INGRESOS']
        CTOTAL = game_data['CTOTAL']
        PRESUPUESTO = game_data['PRESUPUESTO']
        CM = game_data['CM']
        Calm_arr = game_data['Calm']
        ruptadm = game_data['ruptadm']
        Crupt = game_data['Crupt']
        Cnoserv = game_data['Cnoserv']
        duracion = game_data['duracion']
    else:
        # Configurar nueva partida
        print("Introducción de los datos de partida")
        print("Este juego está diseñado para cuatro empresas participantes.")
        print("Las condiciones iniciales serán iguales para cada empresa.")
        print("Los datos introducidos serán la referencia para iniciar la partida.\n")
        
        duracion = enteropos("Escriba la duración del juego en meses: ")
        # Inicialización de matrices para 4 empresas y (duracion+1) meses
        UD = np.zeros((4, duracion+1), dtype=int)
        V = np.zeros((4, duracion+1), dtype=int)
        PVP = np.zeros((4, duracion+1))
        CV = np.zeros((4, duracion+1))
        CF = np.zeros((4, duracion+1), dtype=int)
        ventasmedia = np.zeros((4, 1))
        STOCK = np.zeros((4, duracion+1), dtype=int)
        INGRESOS = np.zeros((4, duracion+1))
        sobran = np.zeros((4, duracion+1), dtype=int)
        faltan = np.zeros((4, duracion+1), dtype=int)
        CTOTAL = np.zeros((4, duracion+1))
        CALM = np.zeros((4, duracion+1), dtype=int)
        Cnoserv = np.zeros((4, duracion+1), dtype=int)
        CRUPT = np.zeros((4, duracion+1), dtype=int)
        VENTASPENDIENTES = np.zeros((4, duracion+1), dtype=int)
        PUB = np.zeros((4, duracion+1))
        mejoras_arr = np.zeros((4, duracion+1))
        
        ventasmax = enteropos("Escriba el valor de la demanda total del mercado: ")
        pvp = positiva("Escriba el precio de venta al público inicial del producto (precio de referencia): ")
        pvpini = pvp
        
        # Inicializar datos para cada empresa (mes 0)
        PRESUPUESTO = np.zeros((4, duracion+1))
        for i in range(4):
            presupuesto = positiva(f"Escriba la cantidad inicial de presupuesto disponible por la empresa {Empresa[i]}: ")
            PRESUPUESTO[i, 0] = presupuesto
            PVP[i, 0] = pvp
            cf = positiva(f"Escriba el coste fijo de la empresa {Empresa[i]}: ")
            CF[i, 0] = int(cf)
            cv = positiva(f"Escriba el coste variable por cada unidad fabricada de la empresa {Empresa[i]}: ")
            CV[i, 0] = cv
            calm = positiva(f"Escriba el coste de almacenamiento por unidad de la empresa {Empresa[i]}: ")
            CALM[i, 0] = int(calm)
            print("En caso de ruptura, ¿Se permite entregar el pedido en el siguiente período?")
            print("1) Escriba 1 en caso afirmativo.")
            print("2) Escriba 2 en caso contrario.")
            ruptadm = unodos()
            if ruptadm == 1:
                cnoserv = positiva(f"Escriba el coste de no servicio de la empresa {Empresa[i]}: ")
                Cnoserv[i, 0] = cnoserv
            else:
                crupt = positiva(f"Escriba el coste de ruptura de la empresa {Empresa[i]}: ")
                CRUPT[i, 0] = int(crupt)
        
        # Matriz de Markov inicial: distribución equitativa
        CM = np.full((4, 4), 0.25)
        
        # Establecer ventas iniciales (mes 0)
        ventasmedia[:] = ventasmax / 4
        V[:, 0] = np.floor(ventasmedia).astype(int).flatten()
        ventasahora = np.sum(V[:, 0])
        ventasquedan = ventasmax - ventasahora
        saco = np.zeros(4, dtype=int)
        while ventasquedan != 0:
            suerte = random.randint(0, 3)
            if saco[suerte] == 0:
                V[suerte, 0] += 1
                ventasquedan -= 1
                saco[suerte] = 1

    # Núcleo del programa: iteración por cada mes (de 1 a duracion)
    for j in range(1, duracion+1):
        print(f"\nComienzo del mes {j}")
        print("-----------------------------------------------------------------")
        # Copiar datos del mes anterior
        PVP[:, j] = PVP[:, j-1]
        CV[:, j] = CV[:, j-1]
        PRESUPUESTO[:, j] = PRESUPUESTO[:, j-1]
        V[:, j] = V[:, j-1]
        STOCK[:, j] = STOCK[:, j-1]
        PUB[:, j] = PUB[:, j-1]
        mejoras_arr[:, j] = mejoras_arr[:, j-1]
        CTOTAL[:, j] = 0
        
        print(f"Se estima que la demanda total del mercado era {ventasmax} en el mes anterior.")
        dem_minima = int(input("Incremento estimado de demanda mínimo (en porcentaje): "))
        while dem_minima < -50 or dem_minima > 200:
            print("La demanda mínima debe estar entre -50 y 200.")
            dem_minima = int(input("Incremento estimado de demanda mínimo (en porcentaje): "))
        
        dem_maxima = int(input("Incremento estimado de demanda máximo (en porcentaje): "))
        while dem_maxima < -50 or dem_maxima > 200 or dem_minima > dem_maxima:
            print("La demanda máxima debe estar entre -50 y 200 e igual o superior a la demanda mínima.")
            dem_maxima = int(input("Incremento estimado de demanda máximo (en porcentaje): "))
        
        demandaminima = round(ventasmax*(100+dem_minima)/100)
        demandamaxima = round(ventasmax*(100+dem_maxima)/100)
        
        # Para cada empresa se solicitan las estrategias para el mes
        for i in range(4):
            print(f"\nEmpresa: {Empresa[i]} - Mes {j}")
            print(f"La demanda del mercado se estima entre {demandaminima} y {demandamaxima}.")
            print(f"Presupuesto actual: {PRESUPUESTO[i, j-1]}")
            print(f"Stock actual: {STOCK[i, j-1]} unidades.")
            print(f"Coste de almacenamiento: {CALM[i, 0]} por unidad.")
            print(f"Coste variable: {CV[i, j-1]}")
            if ruptadm == 2:
                print(f"El cliente no está dispuesto a esperar (coste ruptura: {CRUPT[i, 0]}).")
            else:
                print(f"El cliente está dispuesto a esperar (coste no servicio: {Cnoserv[i, 0]}).")
            UD[i, j] = enteropos(f"¿Cuántas unidades desea poner a la venta para {Empresa[i]} en el mes {j}? ")
            
            modA = None
            # Se permite realizar modificaciones hasta que se seleccione 0 (nada que hacer)
            while modA != 0:
                print(f"\nEstrategia para {Empresa[i]} en el mes {j}:")
                print(f"1) Modificar Precio (actual: {PVP[i, j]})")
                print("2) Invertir en Marketing")
                print("3) Invertir en Mejoras Tecnológicas")
                print("4) Modificar Número de Unidades a vender")
                print("0) No hacer nada")
                modA = int(input("Seleccione una opción: "))
                while modA not in [0, 1, 2, 3, 4]:
                    print("Opción no válida, seleccione 0, 1, 2, 3 o 4.")
                    modA = int(input("Seleccione una opción: "))
                if modA == 1:
                    PVP, CM = precio_vp(PVP, CM, Empresa, i, j, pvpini)
                elif modA == 2:
                    CTOTAL, CM, PUB = marketing(i, j, CM, CTOTAL, PRESUPUESTO, Empresa, PUB, duracion)
                elif modA == 3:
                    CTOTAL, CV, CM, mejoras_arr = mejoras(i, j, CV, CTOTAL, PRESUPUESTO, Empresa, CM, mejoras_arr, duracion)
                elif modA == 4:
                    UD[i, j] = enteropos("¿Cuántas unidades se pondrán a la venta este mes? ")
        
        # Corrección de posibles ventas negativas
        indices_negativos = np.where(V[:, j] < 0)[0]
        if indices_negativos.size > 0:
            V = negativo(V, j, indices_negativos)
        
        # Actualización de la demanda (variación aleatoria)
        aleatorio = random.random()  # valor entre 0 y 1
        porc_suerte = dem_minima + (dem_maxima - dem_minima)*aleatorio
        ventasmax = round(ventasmax*(100+porc_suerte)/100)
        # Cálculo del autovalor unitario de la matriz de Markov
        eigvals, eigvecs = np.linalg.eig(CM)
        cont1 = 0
        for idx, val in enumerate(eigvals):
            if abs(1 - val) < 1e-10:
                cont1 = idx
                break
        PV = eigvecs[:, cont1]
        Norma = np.sum(PV)
        PV = PV / Norma
        ventasmedia = PV * ventasmax
        V[:, j] = np.floor(ventasmedia).astype(int)
        ventasahora = np.sum(V[:, j])
        ventasquedan = ventasmax - ventasahora
        saco = np.zeros(4, dtype=int)
        while ventasquedan > 0:
            suerte = random.randint(0, 3)
            if saco[suerte] == 0:
                V[suerte, j] += 1
                ventasquedan -= 1
                saco[suerte] = 1
        
        # Se combinan las ventas actuales con las pendientes del mes anterior
        Ventasreales = V[:, j] + VENTASPENDIENTES[:, j-1]
        
        for i in range(4):
            if UD[i, j] < Ventasreales[i]:
                faltan[i, j] = Ventasreales[i] - UD[i, j]
                while STOCK[i, j] > 0 and faltan[i, j] > 0:
                    STOCK[i, j] -= 1
                    faltan[i, j] -= 1
                if faltan[i, j] > 0:
                    Ventasreales[i] = Ventasreales[i] - faltan[i, j]
                    if ruptadm == 2:
                        CRUPT[i, j] = faltan[i, j] * CRUPT[i, 0]
                    else:
                        CNOSERV[i, j] = faltan[i, j] * Cnoserv[i, 0]
                        VENTASPENDIENTES[i, j] = faltan[i, j]
                CALM[i, j] = STOCK[i, j] * CALM[i, 0]
            elif UD[i, j] > Ventasreales[i]:
                sobran = UD[i, j] - Ventasreales[i]
                STOCK[i, j] += sobran
                CALM[i, j] = STOCK[i, j] * CALM[i, 0]
            else:
                CALM[i, j] = STOCK[i, j] * CALM[i, 0]
            INGRESOS[i, j] = PVP[i, j] * Ventasreales[i]
            CTOTAL[i, j] += CF[i, 0] + CV[i, j] * UD[i, j] + CALM[i, j] + CRUPT[i, j] + CNOSERV[i, j]
            PRESUPUESTO[i, j] = PRESUPUESTO[i, j] + INGRESOS[i, j] - CTOTAL[i, j]
        
        # Mostrar tablas resumen (se simplifica la presentación)
        print("\nResumen de Producción:")
        for i in range(4):
            print(f"{Empresa[i]} - Unidades fabricadas: {UD[i, j]}, Ventas: {V[i, j]}, Stock: {STOCK[i, j]}")
        
        print("\nResumen de Cuentas:")
        for i in range(4):
            print(f"{Empresa[i]} - Ingresos: {INGRESOS[i, j]}, Costes Totales: {CTOTAL[i, j]}, Presupuesto: {PRESUPUESTO[i, j]}")
        
        # Mostrar gráficas de la matriz de Markov mediante diagramas de pastel
        plt.figure(figsize=(12, 8))
        for i in range(4):
            plt.subplot(2, 2, i+1)
            plt.pie(CM[:, i], labels=Empresa, autopct='%1.1f%%')
            plt.title(f'Probabilidad de cambio de la empresa {Empresa[i]} a:')
        plt.show()
        input("Pulse cualquier tecla para continuar al siguiente mes...")
    
    resultados(V, CM, duracion, UD, PRESUPUESTO, CV)
    
    print("¿Desea guardar la partida?")
    print("1) Escriba 1 para guardar la partida.")
    print("2) Escriba 2 para salir sin guardar la partida.")
    guardar = int(input("Seleccione una opción: "))
    while guardar not in [1, 2]:
        print("Ese valor no es correcto. Escriba 1 o 2.")
        guardar = int(input("Seleccione una opción: "))
    if guardar == 1:
        save_game(UD, V, Ventasreales, VENTASPENDIENTES, PVP, CF, CV, STOCK, CALM, CNOSERV, CRUPT, INGRESOS, CTOTAL, PRESUPUESTO, CM, CALM, ruptadm, Crupt, Cnoserv, j)
    
if __name__ == '__main__':
    main()
