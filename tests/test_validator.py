import unittest
from pathlib import Path
import importlib.util

logic_path = Path(__file__).parent.parent / 'server' / 'logic.py'

spec = importlib.util.spec_from_file_location("logic_module", logic_path)
logic_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logic_module)

is_valid = logic_module.is_valid

class TestValidator(unittest.TestCase):
    """Класс для проверки функции-валидатора"""
    def test_is_valid_simple_expressions(self):
            """Тест валидных выражений"""
            self.assertTrue(is_valid(["1"]))
            self.assertTrue(is_valid(["1", "+", "2"]))
            self.assertTrue(is_valid(["3", "*", "4"]))
            self.assertTrue(is_valid(["5", "/", "6"]))
            self.assertTrue(is_valid(["-", "5"]))
    
    def test_is_valid_with_parentheses(self):
        """Тест выражений со скобками"""
        self.assertTrue(is_valid(["(", "1", "+", "2", ")"]))
        self.assertTrue(is_valid(["(", "1", "+", "2", ")", "*", "3"]))
        self.assertTrue(is_valid(["(", "(", "1", "+", "2", ")", "*", "3", ")"]))
        self.assertTrue(is_valid(["1", "+", "(", "2", "*", "3", ")"]))
    
    def test_is_valid_complex_expressions(self):
        """Тест сложных выражений"""
        self.assertTrue(is_valid(["1", "+", "2", "*", "3", "-", "4", "/", "5"]))
        self.assertTrue(is_valid(["(", "1", "+", "2", ")", "*", "(", "3", "-", "4", ")"]))
        self.assertTrue(is_valid(["-", "1", "*", "(", "2", "+", "3", ")", "-", "4"]))
    
    def test_is_valid_empty(self):
        """Тест невалидных пустых выражений"""
        self.assertFalse(is_valid([]))
    
    def test_is_valid_operator_start(self):
        """Тест выражений, начинающихся с оператора (кроме минуса)"""
        self.assertFalse(is_valid(["+", "1"]))
        self.assertFalse(is_valid(["*", "2"]))
        self.assertFalse(is_valid(["/", "3"]))
    
    def test_is_valid_operator_end(self):
        """Тест выражений, заканчивающихся оператором"""
        self.assertFalse(is_valid(["1", "+"]))
        self.assertFalse(is_valid(["2", "*"]))
        self.assertFalse(is_valid(["3", "-"]))
        self.assertFalse(is_valid(["4", "/"]))
    
    def test_is_valid_double_operators(self):
        """Тест двойных операторов"""
        self.assertFalse(is_valid(["1", "+", "+", "2"]))
        self.assertFalse(is_valid(["3", "*", "-", "4"]))
        self.assertFalse(is_valid(["5", "/", "*", "6"]))
    
    def test_is_valid_invalid_double_numbers(self):
        """Тест двойных чисел без оператора"""
        self.assertFalse(is_valid(["1", "2"]))
        self.assertFalse(is_valid(["3", "4", "+", "5"]))
    
    def test_is_valid_invalid_parentheses(self):
        """Тест невалидных скобок"""
        # Непарные скобки
        self.assertFalse(is_valid(["("]))
        self.assertFalse(is_valid([")"]))
        self.assertFalse(is_valid(["(", "1", "+", "2"]))
        self.assertFalse(is_valid(["1", "+", "2", ")"]))
        
        # Пустые скобки
        self.assertFalse(is_valid(["(", ")"]))
        
        # Неправильный порядок скобок
        self.assertFalse(is_valid([")", "1", "+", "2", "("]))
    
    def test_is_valid_operator_after_parenthesis(self):
        """Тест операторов после закрывающей скобки без числа"""
        self.assertFalse(is_valid(["(", "1", "+", "2", ")", "+"]))
        self.assertFalse(is_valid(["(", "1", "+", "2", ")", "*"]))
    
    def test_is_valid_number_after_parenthesis(self):
        """Тест числа после закрывающей скобки без оператора"""
        self.assertFalse(is_valid(["(", "1", "+", "2", ")", "3"]))
    
    def test_is_valid_edge_cases(self):
        """Тест граничных случаев"""
        # Одиночный минус
        self.assertTrue(is_valid(["-", "5"]))
        
        # Минус в начале выражения
        self.assertTrue(is_valid(["-", "1", "+", "2"]))
        
        # Минус после оператора
        self.assertTrue(is_valid(["1", "+", "-", "2"]))
        self.assertTrue(is_valid(["1", "*", "-", "2"]))

if __name__ == '__main__':
    unittest.main()