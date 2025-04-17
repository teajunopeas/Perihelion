import math

print('Hola mundo')
input('Presiona enter para continuar...')


# Definimos una clase simple llamada Saludo
class Saludo:
    def __init__(self, mensaje):
        self.mensaje = mensaje

    def mostrar(self):
        print(self.mensaje)

# Creamos una instancia de la clase Saludo
saludo = Saludo('Hola desde la clase Saludo!')

# Usamos el método mostrar para imprimir el mensaje
saludo.mostrar()

# Clase más compleja que representa un Círculo

class Circulo:
    def __init__(self, radio):
        self.radio = radio

    def calcular_area(self):
        return math.pi * self.radio ** 2

    def calcular_circunferencia(self):
        return 2 * math.pi * self.radio

# Crear una instancia de Circulo
circulo = Circulo(5)
print(f'Área del círculo: {circulo.calcular_area()}')
print(f'Circunferencia del círculo: {circulo.calcular_circunferencia()}')

# Clase más compleja que representa un Banco con cuentas
class CuentaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self.saldo = saldo

    def depositar(self, cantidad):
        if cantidad > 0:
            self.saldo += cantidad
            print(f'Depositados {cantidad}. Nuevo saldo: {self.saldo}')
        else:
            print('La cantidad a depositar debe ser positiva.')

    def retirar(self, cantidad):
        if 0 < cantidad <= self.saldo:
            self.saldo -= cantidad
            print(f'Retirados {cantidad}. Nuevo saldo: {self.saldo}')
        else:
            print('Fondos insuficientes o cantidad inválida.')

# Crear una instancia de CuentaBancaria
cuenta = CuentaBancaria('Elian', 100)
cuenta.depositar(50)
cuenta.retirar(30)
cuenta.retirar(150)