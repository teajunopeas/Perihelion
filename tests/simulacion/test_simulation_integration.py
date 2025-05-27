import unittest
import os
import numpy as np
from core.simulation import Simulation
from core.company import Company

class TestSimulationIntegration(unittest.TestCase):
    def setUp(self):
        # Setup similar to TestSimulation but with more initial data
        self.empresas = [
            Company({
                'nombre': 'Empresa Test A',
                'presupuesto_inicial': 10000,
                'pvp_inicial': 10,
                'coste_fijo_mensual': 1000,
                'coste_variable_unitario': 5,
                'stock_inicial': 100,
                'coste_almacenamiento_unitario': 1,
                'coste_ruptura_unitario': 2,
                'coste_no_servicio_unitario': 3
            }, ruptadm_global=1),
            Company({
                'nombre': 'Empresa Test B',
                'presupuesto_inicial': 15000,
                'pvp_inicial': 12,
                'coste_fijo_mensual': 1200,
                'coste_variable_unitario': 6,
                'stock_inicial': 150,
                'coste_almacenamiento_unitario': 1.5,
                'coste_ruptura_unitario': 2.5,
                'coste_no_servicio_unitario': 3.5
            }, ruptadm_global=1)
        ]
        self.markov_matrix = np.array([
            [0.8, 0.2],
            [0.3, 0.7]
        ])
        self.demanda_inicial = 1000
        self.simulation = Simulation(self.empresas, self.markov_matrix, self.demanda_inicial, ruptadm_global=1)
        self.test_filename = "test_simulation_state.json"
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.test_filepath = os.path.join(self.data_dir, self.test_filename)

    def tearDown(self):
        # Clean up test file
        if os.path.exists(self.test_filepath):
            try:
                os.remove(self.test_filepath)
            except:
                pass

    def test_simulation_run_and_save(self):
        # Run simulation for 3 months
        num_months = 3
        self.simulation.run_simulation(num_months)
        
        # Verify state
        self.assertEqual(self.simulation.current_month, num_months)
        self.assertTrue(all(len(hist) == num_months + 1 for hist in self.simulation.historial_presupuesto))
        self.assertTrue(all(len(hist) == num_months + 1 for hist in self.simulation.historial_stock))
        self.assertTrue(all(len(hist) == num_months + 1 for hist in self.simulation.historial_ventas))

        # Save state
        self.simulation.save_state(self.test_filepath)
        
        # Verify file exists
        self.assertTrue(os.path.exists(self.test_filepath))

        # Load and verify state matches
        with open(self.test_filepath, 'r', encoding='utf-8') as f:
            import json
            loaded_data = json.load(f)

        # Check key elements
        self.assertEqual(loaded_data['current_month'], self.simulation.current_month)
        self.assertEqual(loaded_data['market_demand'], self.simulation.market_demand)
        self.assertEqual(len(loaded_data['empresas']), len(self.empresas))
        
        # Check company states
        for i, empresa_data in enumerate(loaded_data['empresas']):
            empresa = self.empresas[i]
            self.assertEqual(empresa_data['nombre'], empresa.nombre)
            self.assertEqual(float(empresa_data['presupuesto']), empresa.presupuesto)
            self.assertEqual(float(empresa_data['pvp']), empresa.pvp)
            self.assertEqual(int(empresa_data['stock']), empresa.stock)

        # Check history arrays
        self.assertEqual(len(loaded_data['historial_presupuesto']), len(self.simulation.historial_presupuesto))
        self.assertEqual(len(loaded_data['historial_stock']), len(self.simulation.historial_stock))
        self.assertEqual(len(loaded_data['historial_ventas']), len(self.simulation.historial_ventas))
        self.assertEqual(len(loaded_data['historial_markov']), len(self.simulation.historial_markov))

if __name__ == '__main__':
    unittest.main()
