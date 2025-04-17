import unittest
import numpy as np
from Juego4Empresas.simulador_empresas import economia

class TestEconomia(unittest.TestCase):

    def test_calcular_costos(self):
        self.assertEqual(economia.calcular_costos(100, 10, 5), 150)
        self.assertEqual(economia.calcular_costos(50, 5, 10), 100)
        self.assertEqual(economia.calcular_costos(0, 2, 20), 40)

    def test_calcular_ingresos(self):
        self.assertEqual(economia.calcular_ingresos(50, 10), 500)
        self.assertEqual(economia.calcular_ingresos(25, 20), 500)
        self.assertEqual(economia.calcular_ingresos(100, 5), 500)

    def test_calcular_utilidad(self):
        self.assertEqual(economia.calcular_utilidad(1000, 500), 500)
        self.assertEqual(economia.calcular_utilidad(750, 250), 500)
        self.assertEqual(economia.calcular_utilidad(200, 100), 100)

    def test_calcular_presupuesto(self):
        self.assertEqual(economia.calcular_presupuesto(1000, 500), 500)
        self.assertEqual(economia.calcular_presupuesto(750, 250), 500)
        self.assertEqual(economia.calcular_presupuesto(200, 100), 100)

    def test_calcular_ventas_totales(self):
        V = np.array([[10, 20], [30, 40], [50, 60]])
        expected_result = np.array([30, 70, 110])
        np.testing.assert_array_equal(economia.calcular_ventas_totales(V), expected_result)

if __name__ == '__main__':
    unittest.main()
