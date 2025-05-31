from typing import Dict, List, Union, Optional
from math import sin, log, sqrt, pow
import re
from abc import ABC, abstractmethod


class Expression(ABC):
    """Abstract base class for all expressions."""

    @abstractmethod
    def evaluate(self, variables: Dict[str, float]) -> float:
        """Evaluate the expression with given variables."""
        pass


class Number(Expression):
    """Represents a numeric constant."""

    def __init__(self, value: float):
        self.value = value

    def evaluate(self, variables: Dict[str, float]) -> float:
        return self.value


class Variable(Expression):
    """Represents a variable."""

    def __init__(self, name: str):
        self.name = name

    def evaluate(self, variables: Dict[str, float]) -> float:
        if self.name not in variables:
            raise ValueError(f"Undefined variable: {self.name}")
        return variables[self.name]


class BinaryOperation(Expression):
    """Represents a binary operation (+, -, *, /)."""

    def __init__(self, left: Expression, operator: str, right: Expression):
        self.left = left
        self.operator = operator
        self.right = right

    def evaluate(self, variables: Dict[str, float]) -> float:
        left_val = self.left.evaluate(variables)
        right_val = self.right.evaluate(variables)

        if self.operator == '+':
            return round(left_val + right_val, 10)
        elif self.operator == '-':
            return round(left_val - right_val, 10)
        elif self.operator == '*':
            return round(left_val * right_val, 10)
        elif self.operator == '/':
            if right_val == 0:
                raise ValueError("Division by zero")
            return round(left_val / right_val, 10)
        else:
            raise ValueError(f"Unknown operator: {self.operator}")


class Function(Expression):
    """Represents a function call (pow, log, sin, sqrt, abs)."""

    def __init__(self, name: str, args: List[Expression]):
        self.name = name
        self.args = args

    def evaluate(self, variables: Dict[str, float]) -> float:
        if self.name == 'pow' and len(self.args) == 2:
            return round(pow(self.args[0].evaluate(variables),
                             self.args[1].evaluate(variables)), 10)
        elif self.name == 'log' and len(self.args) == 1:
            arg = self.args[0].evaluate(variables)
            if arg <= 0:
                raise ValueError("Logarithm of non-positive number")
            return round(log(arg), 10)
        elif self.name == 'sin' and len(self.args) == 1:
            return round(sin(self.args[0].evaluate(variables)), 10)
        elif self.name == 'sqrt' and len(self.args) == 1:
            arg = self.args[0].evaluate(variables)
            if arg < 0:
                raise ValueError("Square root of negative number")
            return round(sqrt(arg), 10)
        elif self.name == 'abs' and len(self.args) == 1:
            return round(abs(self.args[0].evaluate(variables)), 10)
        else:
            raise ValueError(
                f"Unknown function or wrong number of arguments: {self.name}")


class Assignment(Expression):
    """Represents a variable assignment."""

    def __init__(self, variable: str, expression: Expression):
        self.variable = variable
        self.expression = expression

    def evaluate(self, variables: Dict[str, float]) -> float:
        value = self.expression.evaluate(variables)
        variables[self.variable] = value
        return value


class Parser:
    """Parser for mathematical expressions."""

    def __init__(self):
        self.tokens = []
        self.current = 0

    def parse(self, expression: str) -> Expression:
        """Parse a mathematical expression."""
        self.tokens = self.tokenize(expression)
        self.current = 0
        return self.parse_expression()

    def tokenize(self, expression: str) -> List[str]:
        """Convert expression string into tokens."""
        pattern = r'([+\-*/()=,;]|[a-zA-Z_][a-zA-Z0-9_]*|\d*\.\d+|\d+)'
        return [token for token in re.findall(pattern, expression) if token.strip()]

    def parse_expression(self) -> Expression:
        """Parse an expression."""
        if self.current < len(self.tokens) - 1 and self.tokens[self.current + 1] == '=':
            variable = self.tokens[self.current]
            self.current += 2
            return Assignment(variable, self.parse_term())
        return self.parse_term()

    def parse_term(self) -> Expression:
        """Parse a term (addition/subtraction)."""
        expr = self.parse_factor()

        while self.current < len(self.tokens):
            if self.tokens[self.current] in '+-':
                operator = self.tokens[self.current]
                self.current += 1
                expr = BinaryOperation(expr, operator, self.parse_factor())
            else:
                break

        return expr

    def parse_factor(self) -> Expression:
        """Parse a factor (multiplication/division)."""
        expr = self.parse_primary()

        while self.current < len(self.tokens):
            if self.tokens[self.current] in '*/':
                operator = self.tokens[self.current]
                self.current += 1
                expr = BinaryOperation(expr, operator, self.parse_primary())
            else:
                break

        return expr

    def parse_primary(self) -> Expression:
        """Parse a primary expression (number, variable, function, or parenthesized expression)."""
        token = self.tokens[self.current]
        self.current += 1

        if token == '(':
            expr = self.parse_expression()
            if self.current >= len(self.tokens) or self.tokens[self.current] != ')':
                raise ValueError("Expected ')'")
            self.current += 1
            return expr

        if token.replace('.', '').isdigit():
            return Number(float(token))

        if token in ['pow', 'log', 'sin', 'sqrt', 'abs']:
            if self.current >= len(self.tokens) or self.tokens[self.current] != '(':
                raise ValueError(f"Expected '(' after function {token}")
            self.current += 1

            args = []
            while True:
                args.append(self.parse_expression())
                if self.current >= len(self.tokens):
                    raise ValueError("Expected ')'")
                if self.tokens[self.current] == ')':
                    self.current += 1
                    break
                if self.tokens[self.current] != ',':
                    raise ValueError("Expected ',' or ')'")
                self.current += 1

            return Function(token, args)

        return Variable(token)


class Calculator:
    """Main calculator class."""

    def __init__(self):
        self.variables: Dict[str, float] = {}
        self.parser = Parser()

    def evaluate_expression(self, expression: str) -> None:
        """Evaluate a mathematical expression."""
        try:
            expressions = [expr.strip()
                           for expr in expression.split(';') if expr.strip()]

            last_result = None
            for expr in expressions:
                current_vars = self.variables.copy()
                expr_obj = self.parser.parse(expr)
                last_result = expr_obj.evaluate(current_vars)
                self.variables.update(current_vars)

            if self.variables:
                print("\nVariables:")
                for var, value in sorted(self.variables.items()):
                    print(f"{var} = {value}")
            else:
                print(f"Result: {last_result}")

        except Exception as e:
            print(f"Error: {str(e)}")
            self.variables.clear()


def main() -> None:
    """Run the calculator program."""
    calculator = Calculator()
    print("Advanced Calculator")
    print("Supported operations: +, -, *, /")
    print("Supported functions: pow, log, sin, sqrt, abs")
    print("Multiple expressions can be separated by ';'")
    print("Enter 'q' to quit")

    while True:
        try:
            expression = input("\nEnter expression: ")
            if expression.lower() == 'q':
                break

            calculator.evaluate_expression(expression)

        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
