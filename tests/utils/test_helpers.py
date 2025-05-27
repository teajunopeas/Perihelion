import unittest
from unittest.mock import patch
import os
from utils import helpers

class TestHelpers(unittest.TestCase):
    @patch('os.system')
    def test_clear_console_windows(self, mock_system):
        with patch('os.name', 'nt'):
            helpers.clear_console()
            mock_system.assert_called_with('cls')

    @patch('os.system')
    def test_clear_console_unix(self, mock_system):
        with patch('os.name', 'posix'):
            helpers.clear_console()
            mock_system.assert_called_with('clear')

    @patch('builtins.input', return_value='1')
    def test_unodos_valid_1(self, mock_input):
        self.assertEqual(helpers.Unodos(), 1)

    @patch('builtins.input', return_value='2')
    def test_unodos_valid_2(self, mock_input):
        self.assertEqual(helpers.Unodos(), 2)

    @patch('builtins.input', side_effect=['3', '2'])
    @patch('builtins.print')
    def test_unodos_invalid_then_valid(self, mock_print, mock_input):
        result = helpers.Unodos()
        self.assertEqual(result, 2)
        mock_print.assert_any_call('Opción no válida. Escriba 1 o 2.')

    @patch('builtins.input', side_effect=['0', '1'])
    @patch('builtins.print')
    def test_unodos_invalid_then_valid_1(self, mock_print, mock_input):
        result = helpers.Unodos()
        self.assertEqual(result, 1)
        mock_print.assert_any_call('Opción no válida. Escriba 1 o 2.')

if __name__ == '__main__':
    unittest.main()
