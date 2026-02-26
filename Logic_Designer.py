# The program is to help me with logic circuits. It should be able to take a formula and simplify it, draw the truth table, and also draw the NAND-only form of the circuit.
# The program should be user-friendly and guide the user through the process of entering the formula and understanding the results.

from sympy import symbols
from sympy.logic.boolalg import simplify_logic
from sympy.parsing.sympy_parser import parse_expr
import itertools
import re


def preprocess_expression(expr):
    """
    Converts logic notation:
    A'B + CD'  ->  (~A & B) | (C & ~D)
    """

    # Replace NOT (A') → ~A
    expr = re.sub(r"([A-Za-z])'", r"~\1", expr)

    # Replace + with |
    expr = expr.replace("+", "|")

    # Insert AND (&) for adjacency:
    # A B → A & B
    expr = re.sub(r"(?<=[A-Za-z\)])(?=[A-Za-z\(~])", "&", expr)

    return expr


def solve_logic_circuit():
    A, B, C, D = symbols('A B C D')
    local_dict = {'A': A, 'B': B, 'C': C, 'D': D}

    print("\n--- Logic Formula Processor ---")
    print("Accepted format example:")
    print("A'(B'C'D + B'CD' + BC'D')")

    user_input = input("\nEnter your formula: ")

    try:
        processed = preprocess_expression(user_input)
        expr = parse_expr(processed, local_dict=local_dict)
        formula = simplify_logic(expr)
    except Exception as e:
        print(f"Error parsing formula: {e}")
        return

    print(f"\n[1] Original Input: {user_input}")
    print(f"[2] Interpreted As: {processed}")
    print(f"[3] Simplified: {formula}")

    draw_truth_table(formula, A, B, C, D)

    draw_diag = input("\nWould you like NAND-only form? (y/n): ").lower()
    if draw_diag == 'y':
        print("\nNAND-only expression:")
        print(convert_to_nand(formula))


def draw_truth_table(formula, A, B, C, D):
    draw_table = input("\nShow truth table? (y/n): ").lower()
    if draw_table == 'y':
        print(f"\n{'A':<3}{'B':<3}{'C':<3}{'D':<3}| Result")
        print("-" * 22)

        for vals in itertools.product([0, 1], repeat=4):
            subs = {A: bool(vals[0]), B: bool(vals[1]),
                    C: bool(vals[2]), D: bool(vals[3])}
            result = int(bool(formula.subs(subs)))
            print(f"{vals[0]:<3}{vals[1]:<3}{vals[2]:<3}{vals[3]:<3}|   {result}")


def convert_to_nand(expr):
    from sympy.logic.boolalg import Not, And, Or

    if expr.is_Symbol:
        return str(expr)

    if isinstance(expr, Not):
        x = convert_to_nand(expr.args[0])
        return f"({x} NAND {x})"

    if isinstance(expr, And):
        x = convert_to_nand(expr.args[0])
        y = convert_to_nand(expr.args[1])
        return f"(({x} NAND {y}) NAND ({x} NAND {y}))"

    if isinstance(expr, Or):
        x = convert_to_nand(expr.args[0])
        y = convert_to_nand(expr.args[1])
        return f"(({x} NAND {x}) NAND ({y} NAND {y}))"

    return str(expr)


if __name__ == "__main__":
    solve_logic_circuit()