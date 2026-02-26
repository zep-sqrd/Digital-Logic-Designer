# To make a program that takes a logic formula from the user and performs the following tasks:

# it simplifies the formula if not already simplified

# asks if the user wants to draw a truth table

# ask if the user want the logic circuit diagram

# ask if the user wants the diagram to fit certain constraints (NAND...)

from sympy import symbols, simplify_logic, sympify
from sympy.logic.boolalg import Not, And, Or, Xor
import itertools

def solve_logic_circuit():
    # Define the variables
    A, B, C, D = symbols('A B C D')

    # User interface
    print("--- Logic Formula Processor (A, B, C, D) ---")
    print("Use: & (AND), | (OR), ~ (NOT), ^ (XOR)")
    user_input = input("Enter your formula (e.g., (A & B) | (~C & D)): ")

    try:
        expr = sympify(user_input)
        formula = simplify_logic(expr)
    except Exception as e:
        print(f"Error parsing formula: {e}")
        return

    # Simplification
    print(f"\n[1] Original Formula: {user_input}")
    print(f"[2] Simplified Formula: {formula}")
    
def draw_truth_table(formula, A, B, C, D):
       
# Draw the truth table

draw_table = input("\nWould you like to see the truth table? (y/n): ").lower()
if draw_table == 'y':
        print(f"{'A':<3} {'B':<3} {'C':<3} {'D':<3} | {'Result'}")
        print("-" * 25)
        
                # Generate all 16 combinations for ABCD
for vals in itertools.product([0, 1], repeat=4):
                    subs = {A: vals[0], B: vals[1], C: vals[2], D: vals[3]}
                    result = 1 if formula.subs(subs) else 0
                    print(f"{vals[0]:<3} {vals[1]:<3} {vals[2]:<3} {vals[3]:<3} | {result}")
        
if __name__ == "__main__":
            solve_logic_circuit()

# Logic Diagram & Constraints

    draw_diag = input("\nWould you like the logic circuit diagram? (y/n): ").lower()
if draw_diag == 'y':
        constraint = input("Fit to certain constraints? (Enter 'NAND' or 'None'): ").upper()
        
        if constraint == "NAND":
            print("\n[Mapping to NAND-only logic...]")
            print("Transformation Rules Applied:")
            print("- NOT(X)    -> (X NAND X)")
            print("- AND(X, Y) -> (X NAND Y) NAND (X NAND Y)")
            print("- OR(X, Y)  -> (X NAND X) NAND (Y NAND Y)")
            # In a real app, you'd use SchemDraw here to render the PNG
            print(f"\nFinal NAND-mapped expression: {convert_to_nand(formula)}")
        else:
            print(f"Generating standard diagram for: {formula}")

def convert_to_nand(expr):
    """Simple string-based representation of NAND conversion."""
    return str(expr).replace('~', 'NAND_INV ').replace('&', ' NAND ').replace('|', ' OR_via_NAND ')

if __name__ == "__main__":
    solve_logic_circuit()
