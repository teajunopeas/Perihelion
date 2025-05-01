import unittest
import numpy as np
from core.simulation import Simulation
from core.company import Company

class TestSimulation(unittest.TestCase):

    def setUp(self):
        # Configuración inicial para las pruebas
        self.empresas = [
            Company({
                'nombre': 'Empresa A',
                'presupuesto_inicial': 10000,
                'pvp_inicial': 10,
                'coste_fijo_mensual': 1000,
                'coste_variable_unitario': 5,
                'stock_inicial': 100,
                'coste_almacenamiento_unitario': 1,
                'coste_ruptura_unitario': 2,
                'coste_no_servicio_unitario': 3
            }, ruptadm=1),
            Company({
                'nombre': 'Empresa B',
                'presupuesto_inicial': 15000,
                'pvp_inicial': 12,
                'coste_fijo_mensual': 1200,
                'coste_variable_unitario': 6,
                'stock_inicial': 150,
                'coste_almacenamiento_unitario': 1.5,
                'coste_ruptura_unitario': 2.5,
                'coste_no_servicio_unitario': 3.5
            }, ruptadm=1)
        ]
        self.markov_matrix = np.array([
            [0.8, 0.2],
            [0.3, 0.7]
        ])
        self.demanda_inicial = 1000
        self.simulation = Simulation(self.empresas, self.markov_matrix, self.demanda_inicial, ruptadm_global=1)

    def test_initialization(self):
        # Verificar que la simulación se inicializa correctamente
        self.assertEqual(self.simulation.num_empresas, 2)
        self.assertEqual(self.simulation.market_demand, self.demanda_inicial)
        self.assertTrue(np.array_equal(self.simulation.markov_matrix, self.markov_matrix))

    def test_validar_y_normalizar_matriz_markov(self):
        # Probar la normalización de la matriz de Markov
        matriz_no_normalizada = np.array([
            [0.5, 0.5],
            [0.0, 0.0]
        ])
        self.simulation._validar_y_normalizar_matriz_markov(matriz_no_normalizada)
        self.assertTrue(np.allclose(np.sum(matriz_no_normalizada, axis=0), 1.0))

    def test_calculate_equilibrium(self):
        # Probar el cálculo del equilibrio de la matriz de Markov
        equilibrium = self.simulation._calculate_equilibrium()
        self.assertAlmostEqual(np.sum(equilibrium), 1.0)
        self.assertTrue(np.all(equilibrium >= 0))

    def test_distribute_demand(self):
        # Probar la distribución de la demanda
        market_share_vector = np.array([0.6, 0.4])
        distributed_demand = self.simulation._distribute_demand(market_share_vector)
        self.assertEqual(np.sum(distributed_demand), self.demanda_inicial)

if __name__ == '__main__':
    unittest.main()