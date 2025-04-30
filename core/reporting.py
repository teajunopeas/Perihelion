import matplotlib.pyplot as plt
import numpy as np

class Reporting:
    def __init__(self, simulation):
        self.sim = simulation
        self.empresa_nombres = [e.nombre for e in simulation.empresas]
        self.meses = list(range(len(simulation.historial_presupuesto[0])))

    def plot_presupuesto(self):
        plt.figure(figsize=(10, 5))
        for i, nombre in enumerate(self.empresa_nombres):
            plt.plot(self.meses, self.sim.historial_presupuesto[i], label=nombre)
        plt.title('Evolución del Presupuesto')
        plt.xlabel('Mes')
        plt.ylabel('Presupuesto (€)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_cuota_mercado(self):
        plt.figure(figsize=(10, 5))
        for i, nombre in enumerate(self.empresa_nombres):
            plt.plot(self.meses, self.sim.historial_cuota_mercado[i], label=nombre)
        plt.title('Evolución de la Cuota de Mercado')
        plt.xlabel('Mes')
        plt.ylabel('Cuota de Mercado')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_ventas(self):
        plt.figure(figsize=(10, 5))
        for i, nombre in enumerate(self.empresa_nombres):
            plt.plot(self.meses, self.sim.historial_ventas[i], label=nombre)
        plt.title('Evolución de Ventas')
        plt.xlabel('Mes')
        plt.ylabel('Ventas (unidades)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_markov_diagonales(self):
        if not hasattr(self.sim, 'historial_markov') or not self.sim.historial_markov:
            print('No hay historial de la matriz de Markov.')
            return
        plt.figure(figsize=(10, 5))
        for i, nombre in enumerate(self.empresa_nombres):
            diag = [m[i, i] for m in self.sim.historial_markov]
            plt.plot(self.meses, diag, label=f"Permanencia {nombre}")
        plt.title('Evolución de la Probabilidad de Permanencia (Markov)')
        plt.xlabel('Mes')
        plt.ylabel('Probabilidad de Permanencia')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_all(self):
        self.plot_presupuesto()
        self.plot_cuota_mercado()
        self.plot_ventas()
        self.plot_markov_diagonales()
