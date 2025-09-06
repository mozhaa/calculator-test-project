import unittest
from pathlib import Path
import importlib.util

logic_path = Path(__file__).parent.parent / 'server' / 'logic.py'

spec = importlib.util.spec_from_file_location("logic_module", logic_path)
logic_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logic_module)

get_tokens = logic_module.get_tokens

class TestInputParser(unittest.TestCase):
    """Класс для проверки правильности разбивки входного выражения на токены"""
    def test_get_tokens_basic_numbers(self):
        """Тест одиночных чисел"""
        self.assertEqual(get_tokens("123"), ["123"])
        self.assertEqual(get_tokens("12.34"), ["12.34"])
        self.assertEqual(get_tokens("0.5"), ["0.5"])
    
    def test_get_tokens_basic_operations(self):
        """Тест базовых операций"""
        self.assertEqual(get_tokens("1+2"), ["1", "+", "2"])
        self.assertEqual(get_tokens("3-4"), ["3", "-", "4"])
        self.assertEqual(get_tokens("5*6"), ["5", "*", "6"])
        self.assertEqual(get_tokens("7/8"), ["7", "/", "8"])
    
    def test_get_tokens_with_spaces(self):
        """Тест выражений с пробелами"""
        self.assertEqual(get_tokens("1 + 2"), ["1", "+", "2"])
        self.assertEqual(get_tokens(" 3 * 4 "), ["3", "*", "4"])
        self.assertEqual(get_tokens("( 1 + 2 ) * 3"), ["(", "1", "+", "2", ")", "*", "3"])
    
    def test_get_tokens_parentheses(self):
        """Тест выражений со скобками"""
        self.assertEqual(get_tokens("(1+2)"), ["(", "1", "+", "2", ")"])
        self.assertEqual(get_tokens("((1+2)*3)"), ["(", "(", "1", "+", "2", ")", "*", "3", ")"])
    
    def test_get_tokens_negative_numbers(self):
        """Тест отрицательных чисел"""
        self.assertEqual(get_tokens("-5"), ["-", "5"])
        self.assertEqual(get_tokens("1 + -2"), ["1", "+", "-", "2"])
        self.assertEqual(get_tokens("3 * -4"), ["3", "*", "-", "4"])
    
    def test_get_tokens_multiple_operations(self):
        """Тест множественных операций"""
        self.assertEqual(get_tokens("1+2+3"), ["1", "+", "2", "+", "3"])
        self.assertEqual(get_tokens("1*2/3"), ["1", "*", "2", "/", "3"])
        self.assertEqual(get_tokens("1+2*3-4/5"), ["1", "+", "2", "*", "3", "-", "4", "/", "5"])
    
    def test_get_tokens_invalid_empty_string(self):
        """Тест невалидных пустых строк"""
        with self.assertRaises(ValueError):
            get_tokens("")
        with self.assertRaises(ValueError):
            get_tokens("   ")
    
    def test_get_tokens_invalid_numbers(self):
        """Тест невалидных чисел"""
        with self.assertRaises(ValueError):
            get_tokens("12.")  # Точка в конце числа
        with self.assertRaises(ValueError):
            get_tokens(".5")   # Точка в начале числа
        with self.assertRaises(ValueError):
            get_tokens("1.2.3")  # Число с двумя точками
    
if __name__ == '__main__':
    unittest.main()
    