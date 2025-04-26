import os

# Limpia la consola de comandos.
def clear_console():
    """
    Limpia la consola de comandos dependiendo del sistema operativo.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


# Función auxilar para recoger la opción del usuario entre dos opciones (1 o 2).
def Unodos(prompt="Elige una opción (1 o 2): ") -> int:
    """
    Pide explicitamente al usuario que introduzca un número 1 o 2, para elegir entre dos opciones.

    Si el usuario introduce un número diferente, se le pide que lo vuelva a intentar.
    Returns:
        int: El número introducido por el usuario (1 o 2).
    """

    choice = input(prompt)
    while choice not in ["1", "2"]:
        print("Opción no válida. Escriba 1 o 2.")
        choice = input("Elige una opción (1 o 2): ")

    return 0 #Placeholder for the function Unodos, which is not defined in the provided code.