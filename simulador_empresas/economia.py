# filepath: c:\Users\elian\OneDrive - Universidad de Las Palmas de Gran Canaria\Curso 24-25 2do semestre\MNF\Trabajo MNF\Juego4Empresas\Juego4Empresas\simulador_empresas\economia.py

def calcular_costos(CF, CV, unidades):
    """
    Calcula el costo total dado el costo fijo, el costo variable y el número de unidades.
    """
    return CF + (CV * unidades)

def calcular_ingresos(PVP, unidades):
    """
    Calcula los ingresos totales dados el precio de venta al público y el número de unidades vendidas.
    """
    return PVP * unidades

def calcular_utilidad(ingresos, costos):
    """
    Calcula la utilidad neta restando los costos de los ingresos.
    """
    return ingresos - costos

def calcular_presupuesto(PRESUPUESTO, gastos):
    """
    Calcula el presupuesto restante después de los gastos.
    """
    return PRESUPUESTO - gastos

def calcular_ventas_totales(V):
    """
    Calcula las ventas totales a partir de la matriz de ventas.
    """
    return V.sum(axis=1)  # Suma las ventas de todas las empresas
