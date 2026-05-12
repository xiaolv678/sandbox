import unittest

from calculator import Calculator, CalculatorError, evaluate


class EvaluateTests(unittest.TestCase):
    def test_basic_arithmetic(self):
        self.assertEqual(evaluate("1 + 2 * 3"), "7")

    def test_parentheses(self):
        self.assertEqual(evaluate("(1 + 2) * 3"), "9")

    def test_decimal_result(self):
        self.assertEqual(evaluate("5 / 2"), "2.5")

    def test_modulo(self):
        self.assertEqual(evaluate("10 % 3"), "1")

    def test_rejects_function_calls(self):
        with self.assertRaises(CalculatorError):
            evaluate("__import__('os').system('echo bad')")

    def test_divide_by_zero(self):
        with self.assertRaises(CalculatorError):
            evaluate("1 / 0")


class CalculatorTests(unittest.TestCase):
    def test_press_sequence(self):
        calculator = Calculator()
        for value in ["1", "+", "2", "="]:
            result = calculator.press(value)
        self.assertEqual(result, "3")

    def test_backspace(self):
        calculator = Calculator()
        for value in ["1", "2", "Backspace"]:
            result = calculator.press(value)
        self.assertEqual(result, "1")

    def test_clear(self):
        calculator = Calculator()
        for value in ["5", "+", "3", "C"]:
            result = calculator.press(value)
        self.assertEqual(result, "")

    def test_press_equals_empty(self):
        calculator = Calculator()
        result = calculator.press("=")
        self.assertEqual(result, "")


class AdditionalEvaluateTests(unittest.TestCase):
    """Additional test cases for comprehensive coverage."""
    
    def test_negative_numbers(self):
        self.assertEqual(evaluate("-5 + 3"), "-2")
    
    def test_power_operator(self):
        self.assertEqual(evaluate("2 ** 3"), "8")
    
    def test_complex_expression(self):
        self.assertEqual(evaluate("5 / 2 * 4"), "10")
    
    def test_nested_parentheses(self):
        self.assertEqual(evaluate("((1 + 2) * 3)"), "9")
    
    def test_floating_point_precision(self):
        # Test that 0.1 + 0.2 displays correctly
        result = evaluate("0.1 + 0.2")
        self.assertEqual(result, "0.3")
    
    def test_large_numbers(self):
        self.assertEqual(evaluate("1000000 * 1000000"), "1e+12")
    
    def test_zero_operations(self):
        self.assertEqual(evaluate("0 + 0"), "0")
        self.assertEqual(evaluate("0 * 100"), "0")
    
    def test_negative_result(self):
        self.assertEqual(evaluate("3 - 5"), "-2")


if __name__ == "__main__":
    unittest.main()
