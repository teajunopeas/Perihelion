import unittest
from core.company import Company

class TestCompany(unittest.TestCase):

    def setUp(self):
        # Configuración inicial para las pruebas
        self.config = {
            'nombre': 'Empresa A',
            'presupuesto_inicial': 10000,
            'pvp_inicial': 10,
            'coste_fijo_mensual': 1000,
            'coste_variable_unitario': 5,
            'stock_inicial': 100,
            'coste_almacenamiento_unitario': 1,
            'coste_ruptura_unitario': 2,
            'coste_no_servicio_unitario': 3
        }
        self.empresa = Company(self.config, ruptadm=1)

    def test_initialization(self):
        # Verificar que la empresa se inicializa correctamente
        self.assertEqual(self.empresa.nombre, 'Empresa A')
        self.assertEqual(self.empresa.presupuesto, 10000)
        self.assertEqual(self.empresa.pvp, 10)
        self.assertEqual(self.empresa.stock, 100)

    def test_decidir_estrategias(self):
        # Probar la decisión de estrategias
        self.empresa.decidir_estrategias(12, 500, 300)
        self.assertEqual(self.empresa.pvp, 12)
        self.assertEqual(self.empresa.marketing_investment, 500)
        self.assertEqual(self.empresa.tech_investment, 300)

    def test_calcular_ventas_y_stock(self):
        # Probar el cálculo de ventas y actualización de stock
        demanda = 80
        uds_no_satisfechas = self.empresa.calcular_ventas_y_stock(demanda)
        self.assertEqual(self.empresa.stock, 20)
        self.assertEqual(uds_no_satisfechas, 0)

if __name__ == '__main__':
    unittest.main()