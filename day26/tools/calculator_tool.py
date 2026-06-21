"""Calculator tool for the Day 26 LangChain ReAct agent.

Evaluates arithmetic expressions safely. Does NOT use Python's built-in
eval(), because eval() will run arbitrary code, not just math - a bad or
malicious input could execute system commands. Instead this parses the
expression into a syntax tree with the ast module and only allows
numeric literals and arithmetic operators through. Anything else
(function calls, imports, attribute access, etc.) is rejected.
"""
import ast
import operator

from langchain_core.tools import tool

# Only these AST operator node types are allowed through _safe_eval.
# Anything not in this dict (function calls, comparisons, etc.) raises.
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node: ast.AST) -> float:
    """Recursively evaluate an arithmetic-only AST node.

    Args:
        node: An ast node, e.g. the body of ast.parse(expr, mode="eval").

    Returns:
        The numeric result.

    Raises:
        ValueError: If the node is anything other than a number,
            a binary arithmetic operation, or a unary +/-.
    """
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant: {node.value!r}")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator not allowed: {op_type.__name__}")
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return _ALLOWED_OPERATORS[op_type](left, right)

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError(f"Operator not allowed: {op_type.__name__}")
        return _ALLOWED_OPERATORS[op_type](_safe_eval(node.operand))

    raise ValueError(f"Unsupported expression node: {ast.dump(node)}")


@tool
def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression and return the result.

    Use this tool whenever the user asks for a calculation, such as
    "23 * 45" or "(10 + 5) / 3". Supports +, -, *, /, ** (power),
    % (modulo) and parentheses. Does NOT support variables, functions
    (like sqrt), or anything beyond plain arithmetic.

    Args:
        expression: A math expression as a string, e.g. "23 * 45".

    Returns:
        The computed result as a string, or a message starting with
        "Error:" if the expression could not be evaluated.
    """
    try:
        parsed = ast.parse(expression, mode="eval")
        result = _safe_eval(parsed.body)
        return str(result)
    except ZeroDivisionError:
        return "Error: division by zero."
    except (SyntaxError, ValueError, TypeError) as exc:
        return f"Error: could not evaluate '{expression}' ({exc})."


if __name__ == "__main__":
    # Quick manual smoke test. Run this file directly (python
    # tools/calculator_tool.py) to sanity check the tool before it's
    # wired into an agent. Includes a malicious-looking input to prove
    # the safety restriction actually works.
    test_cases = [
        "23 * 45",
        "(10 + 5) / 3",
        "2 ** 10",
        "10 / 0",
        "__import__('os').system('echo hacked')",
    ]
    for case in test_cases:
        outcome = calculator.invoke({"expression": case})
        print(f"{case!r} -> {outcome}")