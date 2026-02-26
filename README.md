# Logic Circuit Processor (ABCD)

A bad Python Utility.

## Features
* **Formula Simplification:** Uses SymPy to reduce complex logic (e.g., `A & (A | B)`) to its simplest form.
* **Variable Support:** Specifically optimized for variables **A, B, C, and D**.
* **Truth Table Generation:** Automatically generates a 16-row truth table ($2^4$ combinations).
* **NAND-Only Mapping:** Converts any logic gate into its universal NAND-gate equivalent.
* **Visual Diagrams:** Generates circuit diagrams using the `SchemDraw` library.

## Installation

1. Ensure you have [Python 3.x](https://www.python.org/) installed.
2. Install the required dependencies:
   ```bash
   pip install sympy schemdraw matplotlib
