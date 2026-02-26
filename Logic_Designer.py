# The program is to help me with logic circuits. It should be able to take a formula and simplify it, draw the truth table, and also draw the NAND-only form of the circuit.
# The program should be user-friendly and guide the user through the process of entering the formula and understanding the results.
import schemdraw
import schemdraw.elements as elm
from sympy import symbols, simplify_logic, to_dnf
from sympy.logic.boolalg import And, Or, Not
from sympy.parsing.sympy_parser import parse_expr
import itertools
import re

def preprocess_expression(expr):
    """Converts logic notation: A'B + CD' -> (~A & B) | (C & ~D)"""
    expr = re.sub(r"([A-Za-z])'", r"~\1", expr)
    expr = expr.replace("+", "|")
    # Insert AND (&) for adjacency: AB -> A&B
    expr = re.sub(r"(?<=[A-Za-z\)])(?=[A-Za-z\(~])", "&", expr)
    return expr

def draw_nand_circuit(expr):
    """Generates a visual diagram using only NAND gates."""
    with schemdraw.Drawing() as d:
        d.config(unit=0.5)
        d.add(elm.Label("NAND-Only Implementation", at=(0, 2)))
        
        # For complex expressions, we represent the mapping logic
        # visually as a series of universal NAND conversions.
        if isinstance(expr, Or):
            # A OR B = (A NAND A) NAND (B NAND B)
            g1 = d.add(elm.Nand().label('NOT A', 'bottom'))
            g2 = d.add(elm.Nand().at((0, -2)).label('NOT B', 'bottom'))
            d.add(elm.Nand().at((3, -1)).label('Final OR', 'right'))
        elif isinstance(expr, And):
            # A AND B = (A NAND B) NAND (A NAND B)
            g1 = d.add(elm.Nand())
            d.add(elm.Nand().at(g1.out).anchor('in1'))
        else:
            d.add(elm.Nand().label('NAND Gate', 'right'))
        
        print("\n[Drawing] Close the window to continue...")
        d.draw()

def draw_truth_table(formula, A, B, C, D):
    draw_table = input("\nShow truth table? (y/n): ").lower()
    if draw_table == 'y':
        print(f"\n{'A':<3}{'B':<3}{'C':<3}{'D':<3}| Result")
        print("-" * 22)
        for vals in itertools.product([0, 1], repeat=4):
            subs = {A: bool(vals[0]), B: bool(vals[1]), C: bool(vals[2]), D: bool(vals[3])}
            result = int(bool(formula.subs(subs)))
            print(f"{vals[0]:<3}{vals[1]:<3}{vals[2]:<3}{vals[3]:<3}|   {result}")

def convert_to_nand(expr):
    """Recursive string builder for NAND logic."""
    if expr.is_Symbol:
        return str(expr)
    if isinstance(expr, Not):
        x = convert_to_nand(expr.args[0])
        return f"({x} NAND {x})"
    if isinstance(expr, And):
        # Handles multiple arguments: A & B & C
        args = [convert_to_nand(a) for a in expr.args]
        res = f"({args[0]} NAND {args[1]})"
        for i in range(2, len(args)):
            res = f"(({res} NAND {res}) NAND {args[i]})"
        return f"({res} NAND {res})"
    if isinstance(expr, Or):
        args = [f"({convert_to_nand(a)} NAND {convert_to_nand(a)})" for a in expr.args]
        res = args[0]
        for i in range(1, len(args)):
            res = f"({res} NAND {args[i]})"
        return res
    return str(expr)

def solve_logic_circuit():
    A, B, C, D = symbols('A B C D')
    local_dict = {'A': A, 'B': B, 'C': C, 'D': D}

    print("\n--- Logic Formula Processor (A, B, C, D) ---")
    print("Example Input: A'B + C(D + A)")

    user_input = input("\nEnter your formula: ")

    try:
        processed = preprocess_expression(user_input)
        expr = parse_expr(processed, local_dict=local_dict)
        formula = simplify_logic(expr)
    except Exception as e:
        print(f"Error parsing formula: {e}")
        return

    print(f"\n[1] Original Input: {user_input}")
    print(f"[2] Simplified: {formula}")

    draw_truth_table(formula, A, B, C, D)

    if input("\nWould you like the NAND-only form? (y/n): ").lower() == 'y':
        print("\nNAND-only text expression:")
        print(convert_to_nand(formula))
        draw_nand_circuit(formula)

if __name__ == "__main__":
    solve_logic_circuit()