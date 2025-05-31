from typing import Union, Dict, Callable


def calculate(expression: str) -> Union[float, bool, str]:
    """Calculate the result of a mathematical expression.

    Args:
        expression (str): A string containing two numbers and an operator
            in format 'num_left operator num_right'.

    Returns:
        Union[float, bool, str]: The result of the calculation. Returns float for arithmetic
            operations, bool for comparison operations, or str for error messages.

    Raises:
        ValueError: If the expression format is invalid, numbers are invalid,
            or operator is not supported.
    """

    parts = expression.strip().split()

    if len(parts) != 3:
        raise ValueError(
            "Invalid expression format. Expected: 'num_left operator num_right'")

    try:
        num_left = float(parts[0])
        operator = parts[1]
        num_right = float(parts[2])
    except ValueError:
        raise ValueError("Invalid numbers in expression")

    # Dictionary of supported operations
    operations: Dict[str, Callable[[float, float], Union[float, bool, str]]] = {
        '+': lambda x, y: round(x + y, 10),
        '-': lambda x, y: round(x - y, 10),
        '*': lambda x, y: round(x * y, 10),
        '/': lambda x, y: round(x / y, 10) if y != 0 else "Error: Division by zero",
        '<': lambda x, y: x < y,
        '>': lambda x, y: x > y,
        '<=': lambda x, y: x <= y,
        '>=': lambda x, y: x >= y,
        '!=': lambda x, y: x != y,
        '==': lambda x, y: x == y
    }

    if operator not in operations:
        raise ValueError(f"Unsupported operator: {operator}")

    result = operations[operator](num_left, num_right)
    return result


def main() -> None:
    """Run the main calculator program loop.

    Continuously prompts for input until 'q' is entered.
    Handles user input and displays results or error messages.
    """
    print("Simple Calculator")
    print("Enter expression in format: 'num_left operator num_right'")
    print("Supported operators: +, -, *, /, <, >, <=, >=, !=, ==")
    print("Enter 'q' to quit")

    while True:
        try:
            expression = input("\nEnter expression: ")
            if expression.lower() == 'q':
                break

            result = calculate(expression)
            print(f"Result: {result}")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
