import ast
import operator


class CalculatorError(Exception):
    """Raised when a calculator expression cannot be evaluated."""


class Calculator:
    def __init__(self):
        self.expression = ""

    def press(self, value):
        if value == "C":
            self.expression = ""
            return self.expression

        if value == "Backspace":
            self.expression = self.expression[:-1]
            return self.expression

        if value == "=":
            self.expression = evaluate(self.expression)
            return self.expression

        self.expression += value
        return self.expression


def evaluate(expression):
    expression = expression.strip()
    if not expression:
        return ""

    try:
        tree = ast.parse(expression, mode="eval")
        value = _eval_node(tree.body)
    except CalculatorError:
        raise
    except Exception as exc:
        raise CalculatorError("Invalid expression") from exc

    return _format_number(value)


def _eval_node(node):
    binary_ops = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }
    unary_ops = {
        ast.UAdd: operator.pos,
        ast.USub: operator.neg,
    }

    # Handle both ast.Constant (Python 3.8+) and ast.Num (Python 3.7 and earlier)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    
    # Support for Python 3.7 and earlier
    if isinstance(node, ast.Num) and isinstance(node.n, (int, float)):
        return node.n

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in binary_ops:
            raise CalculatorError("Unsupported operator")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        try:
            return binary_ops[op_type](left, right)
        except ZeroDivisionError as exc:
            raise CalculatorError("Cannot divide by zero") from exc

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in unary_ops:
            raise CalculatorError("Unsupported operator")
        return unary_ops[op_type](_eval_node(node.operand))

    raise CalculatorError("Unsupported expression")


def _format_number(value):
    if not isinstance(value, (int, float)):
        raise CalculatorError("Invalid result")

    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    
    # Handle floating-point precision issues
    # Round to 12 significant digits to avoid display artifacts
    if isinstance(value, float):
        # Round to avoid floating-point precision artifacts (e.g., 0.1 + 0.2)
        rounded = round(value, 12)
        if rounded.is_integer():
            return str(int(rounded))
        formatted = f"{rounded:.12g}"
        return formatted

    return f"{value:.12g}"
