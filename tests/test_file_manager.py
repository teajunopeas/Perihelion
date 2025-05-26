import unittest
import os
import numpy as np
from core.simulation import Simulation
from core.company import Company
from utils.file_manager import save_game, validate_filename
import json

class TestFileManager(unittest.TestCase):
    def setUp(self):
        # Setup similar to TestSimulation
        self.empresas = [
            Company({
                'nombre': 'Empresa Test',
                'presupuesto_inicial': 10000,
                'pvp_inicial': 10,
                'coste_fijo_mensual': 1000,
                'coste_variable_unitario': 5,
                'stock_inicial': 100,
                'coste_almacenamiento_unitario': 1,
                'coste_ruptura_unitario': 2,
                'coste_no_servicio_unitario': 3
            }, ruptadm_global=1)
        ]
        self.markov_matrix = np.array([[1.0]])
        self.demanda_inicial = 1000
        self.simulation = Simulation(self.empresas, self.markov_matrix, self.demanda_inicial, ruptadm_global=1)
        self.test_filename = "test_save_state.json"

    def tearDown(self):
        # Clean up any test files
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        test_file = os.path.join(data_dir, self.test_filename)
        if os.path.exists(test_file):
            os.remove(test_file)

    def test_save_and_load_state(self):
        # Save current state
        state_data = self.simulation.to_dict()
        save_game(state_data, self.test_filename)

        # Verify file exists
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        saved_file = os.path.join(data_dir, self.test_filename)
        self.assertTrue(os.path.exists(saved_file))

        # Load and verify state
        with open(saved_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)        # Check key state elements
        self.assertEqual(loaded_data['current_month'], self.simulation.current_month)
        self.assertEqual(loaded_data['market_demand'], self.simulation.market_demand)
        self.assertEqual(len(loaded_data['empresas']), len(self.empresas))

        # Check company data
        company_data = loaded_data['empresas'][0]
        test_company = self.empresas[0]
        self.assertEqual(company_data['nombre'], test_company.nombre)
        self.assertEqual(company_data['presupuesto'], test_company.presupuesto)
        self.assertEqual(company_data['pvp'], test_company.pvp)
        self.assertEqual(company_data['stock'], test_company.stock)

    def test_validate_filename(self):
        # Test valid filename
        valid_name = "test.json"
        self.assertEqual(validate_filename(valid_name), valid_name)

        # Test filename without extension
        no_ext = "test"
        self.assertEqual(validate_filename(no_ext), no_ext + ".json")

        # Test filename with wrong extension
        wrong_ext = "test.txt"
        self.assertEqual(validate_filename(wrong_ext), "test.json")

if __name__ == '__main__':
    unittest.main()
