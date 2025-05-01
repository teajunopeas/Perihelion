import os

# Limpia la consola de comandos.
def clear_console():
    """
    Limpia la consola de comandos dependiendo del sistema operativo.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


# Función auxilar para recoger la opción del usuario entre dos opciones (1 o 2).
def Unodos(prompt="Elige una opción (1 o 2): ", choose_btwn = None) -> int:
    """
    Pide explicitamente al usuario que introduzca un número 1 o 2, para elegir entre dos opciones.
    Si el usuario introduce un número diferente, se le pide que lo vuelva a intentar.

    Args:
        prompt (str): Mensaje que se muestra al usuario para elegir una opción.
        opciones (list, optional): Lista con las opciones a mostrar. 
            Por ejemplo: ["Cargar partida", "Nueva partida"]

    Returns:
        int: El número introducido por el usuario (1 o 2).
    """
    if choose_btwn is not None:
        for i, option in enumerate(choose_btwn,1):
            print(f"{i}. {option}")
        print()

    choice = input(prompt)
    while choice not in ["1", "2"]:
        print("Opción no válida. Escriba 1 o 2.")
        choice = input("Elige una opción (1 o 2): ")

    return int(choice)