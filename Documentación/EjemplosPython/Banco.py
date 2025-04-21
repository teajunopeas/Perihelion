class CuentaBancaria:
    def __init__(self, titular: str, saldo=0):
        assert saldo >= 0, "El saldo de la cuenta no puede ser negativo"

        self.titular = titular
        self.saldo = saldo

    # Métod0 para añadir la cantidad a la cuenta bancaria
    def depositar(self, cantidad):
        assert cantidad > 0, "La cantidad añadida debe ser mayor a 0"

        self.saldo += cantidad

    #Métod0 para retirar la cantidad de la cuenta bancaria
    def retirar(self, cantidad):
        assert cantidad > 0, "La cantidad añadida debe ser mayor a 0"
        assert self.saldo >= cantidad, f"El saldo actual ({self.saldo}), es menor que la cantidad a retirar, abortando operación"

        self.saldo -= cantidad

    def __str__(self):
        return f"Cuenta de {self.titular} - Saldo disponible: {self.saldo} $"

Cuenta = CuentaBancaria("Benito López")

Cuenta.depositar(700)
print(Cuenta)

Cuenta.retirar(100)
print(Cuenta)

#Tratar de retirar más de la cuenta
try:
    Cuenta.retirar(1000)
except Exception as e:
    print(e)

# Introducir una cantidad negativa
try:
    Cuenta.depositar(-20)
except Exception as e:
    print(e)