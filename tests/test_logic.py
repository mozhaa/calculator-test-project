import unittest
from pathlib import Path
import importlib.util

logic_path = Path(__file__).parent.parent / 'server' / 'logic.py'

spec = importlib.util.spec_from_file_location("logic_module", logic_path)
logic_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logic_module)

calculate = logic_module.calculate

class TestCalculation(unittest.TestCase):
    """Класс для проверки правильности счёта калькулятора"""
    def test_calculate_basic(self):
        """Тест базовых арифметических операций"""
        self.assertAlmostEqual(calculate("1 + 2"), 3.0)
        self.assertAlmostEqual(calculate("3 - 4"), -1.0)
        self.assertAlmostEqual(calculate("5 * 6"), 30.0)
        self.assertAlmostEqual(calculate("8 / 4"), 2.0)
        self.assertAlmostEqual(calculate("10 / 3"), 3.3333333333333334)
    
    def test_calculate_decimal(self):
        """Тест операций с десятичными числами"""
        self.assertAlmostEqual(calculate("2.5 + 3.5"), 6.0)
        self.assertAlmostEqual(calculate("7.2 - 2.1"), 5.1)
        self.assertAlmostEqual(calculate("2.5 * 4"), 10.0)
        self.assertAlmostEqual(calculate("9.6 / 2.4"), 4.0)
        self.assertAlmostEqual(calculate("0.1 + 0.2"), 0.3)
        self.assertAlmostEqual(calculate("3.14159 * 2"), 6.28318)
        self.assertAlmostEqual(calculate("10.5 / 2.5"), 4.2)
    
    def test_calculate_operator_order(self):
        """Тест приоритета операторов"""
        self.assertAlmostEqual(calculate("2 + 3 * 4"), 14.0)
        self.assertAlmostEqual(calculate("2 * 3 + 4"), 10.0)          
        self.assertAlmostEqual(calculate("8 / 4 * 2"), 4.0)           
        self.assertAlmostEqual(calculate("2 + 3 * 4 - 5"), 9.0)      
        self.assertAlmostEqual(calculate("10 - 6 / 2"), 7.0)    
        self.assertAlmostEqual(calculate("4 * 3 / 2 + 1"), 7.0)
        self.assertAlmostEqual(calculate("1 + 2 * 3 * 4"), 25.0)       
    
    def test_calculate_with_parentheses(self):
        """Тест выражений со скобками"""
        self.assertAlmostEqual(calculate("(1 + 2)"), 3.0)
        self.assertAlmostEqual(calculate("(1 + 2) * 3"), 9.0)
        self.assertAlmostEqual(calculate("2 * (3 + 4)"), 14.0)
        self.assertAlmostEqual(calculate("(2 + 3) * (4 - 1)"), 15.0)
        self.assertAlmostEqual(calculate("((1 + 2) * 3)"), 9.0)
        self.assertAlmostEqual(calculate("(5 * (2 + 3)) / 5"), 5.0)
        self.assertAlmostEqual(calculate("(1 + (2 * (3 + 4)))"), 15.0)
        self.assertAlmostEqual(calculate("((2 + 3) * 4) - 1"), 19.0)
    
    def test_calculate_negative_numbers(self):
        """Тест отрицательных чисел"""
        self.assertAlmostEqual(calculate("-5"), -5.0)
        self.assertAlmostEqual(calculate("1 + (-2)"), -1.0)
        self.assertAlmostEqual(calculate("3 * (-4)"), -12.0)
        self.assertAlmostEqual(calculate("-8 / 2"), -4.0)
        self.assertAlmostEqual(calculate("(-5 + 3)"), -2.0)
        self.assertAlmostEqual(calculate("2 - (-3)"), 5.0)
        self.assertAlmostEqual(calculate("-2 * (-3)"), 6.0)
        self.assertAlmostEqual(calculate("10 / (-2)"), -5.0)
        self.assertAlmostEqual(calculate("-(2 + 3)"), -5.0)
    
    def test_calculate_complex_expressions(self):
        """Тест сложных выражений"""
        self.assertAlmostEqual(calculate("1 + 2 * 3 - 4 / 2"), 5.0)
        self.assertAlmostEqual(calculate("(1 + 2) * (3 - 4) / 5"), -0.6)
        self.assertAlmostEqual(calculate("2.5 * (3 + 1.5) - 4 / 2"), 9.25)
        self.assertAlmostEqual(calculate("10 / (2 + 3) * 4 - 1"), 7.0)
        self.assertAlmostEqual(calculate("3 * (4 + 2) / (5 - 2)"), 6.0)
        self.assertAlmostEqual(calculate("(1 + 2 * 3) / (4 - 1)"), 2.3333333333333335)
    
    def test_calculate_edge_cases(self):
        """Тест граничных случаев"""
        self.assertAlmostEqual(calculate("0"), 0.0)
        self.assertAlmostEqual(calculate("0.0"), 0.0)
        self.assertAlmostEqual(calculate("1"), 1.0)
        self.assertAlmostEqual(calculate("3.14159"), 3.14159)
        self.assertAlmostEqual(calculate("1 + 0"), 1.0)
        self.assertAlmostEqual(calculate("0 * 5"), 0.0)
        self.assertAlmostEqual(calculate("1 * 1"), 1.0)
        self.assertAlmostEqual(calculate("999999999"), 999999999.0)
        self.assertAlmostEqual(calculate("0.000001"), 0.000001)
    
    def test_calculate_with_spaces(self):
        """Тест выражений с пробелами"""
        self.assertAlmostEqual(calculate("  1  +  2  "), 3.0)
        self.assertAlmostEqual(calculate("( 1 + 2 ) * 3"), 9.0)
        self.assertAlmostEqual(calculate("  2.5  *  ( 3  +  1.5  )  "), 11.25)
        self.assertAlmostEqual(calculate("  -5  +  3  "), -2.0)
        self.assertAlmostEqual(calculate("1+2"), 3.0)
        self.assertAlmostEqual(calculate("1 +2"), 3.0)
        self.assertAlmostEqual(calculate("1+ 2"), 3.0)
    
    def test_calculate_large_numbers(self):
        """Тест больших чисел"""
        self.assertAlmostEqual(calculate("1000000 + 2000000"), 3000000.0)
        self.assertAlmostEqual(calculate("999999 * 2"), 1999998.0)
        self.assertAlmostEqual(calculate("1000000 / 1000"), 1000.0)
        self.assertAlmostEqual(calculate("123456789 + 1"), 123456790.0)
    
    def test_calculate_small_numbers(self):
        """Тест малых чисел"""
        self.assertAlmostEqual(calculate("0.000001 + 0.000002"), 0.000003)
        self.assertAlmostEqual(calculate("0.0001 * 0.01"), 0.000001)
    
    def test_calculate_nested_parentheses(self):
        """Тест вложенных скобок"""
        self.assertAlmostEqual(calculate("((1 + 2) * (3 + 4))"), 21.0)
        self.assertAlmostEqual(calculate("(2 * (3 + (4 * 2)))"), 22.0)
        self.assertAlmostEqual(calculate("((5 - 1) * (2 + (3 / 1)))"), 20.0)

    def test_division_by_zero_direct(self):
        """Тест деления на ноль"""
        with self.assertRaises(ValueError):
            calculate("5 / 0")
        
        with self.assertRaises(ValueError):
            calculate("0 / 0")
    
        with self.assertRaises(ValueError):
            calculate("10 / (5 - 5)")
        
        with self.assertRaises(ValueError):
            calculate("(2 + 3) / (10 - 10)")

        with self.assertRaises(ValueError):
            calculate("((2 + 3) / 0)")
    
if __name__ == '__main__':
    unittest.main()