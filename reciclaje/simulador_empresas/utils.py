# utils.py

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
            valor = int(input(prompt))
            if valor > 0:
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