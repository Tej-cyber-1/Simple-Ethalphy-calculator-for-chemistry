import re
from fractions import Fraction
from math import gcd

# Global CONSTANT (allowed): standard enthalpies of formation at 298 K, kJ/mol.
# Approximate textbook (CRC-style) values. Elements in their standard state are 0.
# Add a phase like "H2O(g)" if you want the gas version; plain "H2O" is liquid.
ENTHALPY_OF_FORMATION = {
    "H2": 0.0, "O2": 0.0, "N2": 0.0, "Cl2": 0.0, "C": 0.0, "S": 0.0,
    "Na": 0.0, "Mg": 0.0, "Al": 0.0, "Ca": 0.0, "Fe": 0.0,
    "H2O": -285.8, "H2O(g)": -241.8, "H2O2": -187.8,
    "CO2": -393.5, "CO": -110.5,
    "CH4": -74.6, "C2H6": -84.0, "C3H8": -103.8, "C4H10": -125.6,
    "C2H4": 52.4, "C2H2": 227.4,
    "CH3OH": -238.7, "C2H5OH": -277.7, "C6H12O6": -1273.3,
    "NH3": -45.9, "NO": 91.3, "NO2": 33.2, "N2O": 82.1,
    "SO2": -296.8, "SO3": -395.7, "H2S": -20.6, "HCl": -92.3,
    "NaCl": -411.2, "CaO": -635.1, "CaCO3": -1206.9, "MgO": -601.6,
    "Fe2O3": -824.2, "Al2O3": -1675.7, "O3": 142.7,
}


def get_species_data(formula: str) -> float:
    """Return the standard enthalpy of formation (kJ/mol) for a formula."""
    if formula not in ENTHALPY_OF_FORMATION:
        raise ValueError(f"No data for '{formula}'. Known: "
                         + ", ".join(sorted(ENTHALPY_OF_FORMATION)))
    return ENTHALPY_OF_FORMATION[formula]


def parse_formula(formula: str) -> dict:
    """'C2H6' -> {'C': 2, 'H': 6}. A phase tag like '(g)' is ignored."""
    clean = re.sub(r"\((g|l|s|aq)\)$", "", formula)
    # Advanced technique: re.findall with a regex pattern.
    # Each match is (element symbol, optional count), e.g. ('H', '2').
    pieces = re.findall(r"([A-Z][a-z]?)(\d*)", clean)
    if not pieces or "".join(e + n for e, n in pieces) != clean:
        raise ValueError(f"Can't read formula '{formula}'")
    counts = {}
    for element, number in pieces:
        counts[element] = counts.get(element, 0) + (int(number) if number else 1)
    return counts


def balance_equation(reactants: list[str], products: list[str]):
    """
    Balance a reaction. Returns (reactant_coeffs, product_coeffs) as dicts.

    Advanced technique: we set up one equation per element
    (atoms in = atoms out) and solve the linear system with Gaussian
    elimination using Fractions, so there are no rounding errors.
    """
    species = reactants + products
    parsed = [parse_formula(s) for s in species]
    elements = sorted({e for p in parsed for e in p})

    # Rows = elements, columns = species. Products count as negative.
    rows = []
    for element in elements:
        row = []
        for i, atoms in enumerate(parsed):
            sign = 1 if i < len(reactants) else -1
            row.append(Fraction(sign * atoms.get(element, 0)))
        rows.append(row)

    # Reduce to row-echelon form.
    pivots = []
    r = 0
    for c in range(len(species)):
        pivot_row = None
        for i in range(r, len(rows)):
            if rows[i][c] != 0:
                pivot_row = i
                break
        if pivot_row is None:
            continue
        rows[r], rows[pivot_row] = rows[pivot_row], rows[r]
        pivot_value = rows[r][c]
        rows[r] = [x / pivot_value for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                factor = rows[i][c]
                rows[i] = [a - factor * b for a, b in zip(rows[i], rows[r])]
        pivots.append(c)
        r += 1
        if r == len(rows):
            break

    free = [c for c in range(len(species)) if c not in pivots]
    if len(free) != 1:
        raise ValueError("These compounds can't be balanced into one unique equation.")

    solution = [Fraction(0)] * len(species)
    solution[free[0]] = Fraction(1)
    for row_index, pivot_col in enumerate(pivots):
        solution[pivot_col] = -rows[row_index][free[0]]

    # Scale to the smallest whole numbers.
    multiple = 1
    for x in solution:
        multiple = multiple * x.denominator // gcd(multiple, x.denominator)
    whole = [int(x * multiple) for x in solution]
    divisor = 0
    for x in whole:
        divisor = gcd(divisor, abs(x))
    whole = [x // divisor for x in whole]

    if any(x <= 0 for x in whole):
        raise ValueError("These compounds can't be balanced (check which side each goes on).")

    n_reactants = len(reactants)
    reac = dict(zip(reactants, whole[:n_reactants]))
    prod = dict(zip(products, whole[n_reactants:]))
    return reac, prod