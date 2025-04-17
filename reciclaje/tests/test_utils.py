import unittest
from unittest.mock import patch
from io import StringIO
from Juego4Empresas.simulador_empresas import utils

class TestUtils(unittest.TestCase):

    @patch('builtins.input', return_value='1')
    def test_unodos_valid_input(self, mock_input):
        self.assertEqual(utils.unodos("Prompt:"), 1)

    @patch('builtins.input', side_effect=['3', '1'])
    def test_unodos_invalid_then_valid_input(self, mock_input):
        self.assertEqual(utils.unodos("Prompt:"), 1)

    @patch('builtins.input', return_value='5')
    def test_enteropos_valid_input(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            self.assertEqual(utils.enteropos("Prompt:"), '5')

    @patch('builtins.input', side_effect=['-1', '1'])
    def test_enteropos_invalid_then_valid_input(self, mock_input):
        with patch('sys.stdout', new_callable=StringIO) as stdout:
            self.assertEqual(utils.enteropos("Prompt:"), '1')

    @patch('builtins.input', return_value='5.5')
    def test_positiva_valid_input(self, mock_input):
        self.assertEqual(utils.positiva("Prompt:"), 5.5)

    @patch('builtins.input', side_effect=['-1', '1.5'])
    def test_positiva_invalid_then_valid_input(self, mock_input):
        self.assertEqual(utils.positiva("Prompt:"), 1.5)

if __name__ == '__main__':
    unittest.main()
