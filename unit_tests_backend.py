# ============================================================
# PASTE THIS AT THE BOTTOM of backend.py
# 
# ============================================================
from bakery import assert_equal


def raises_value_error(function, *arguments) -> bool:
    """Return True if calling function(*arguments) raises a ValueError.

    Test helper: lets us check error cases without crashing the test run.
    """
    try:
        function(*arguments)
    except ValueError:
        return True
    return False


# ---------- get_species_data ----------
assert_equal(get_species_data("H2O"), -285.8)
assert_equal(get_species_data("H2O(g)"), -241.8)
assert_equal(get_species_data("O2"), 0.0)
assert_equal(raises_value_error(get_species_data, "Xyz"), True)

# ---------- parse_formula ----------
assert_equal(parse_formula("H2O"), {"H": 2, "O": 1})
assert_equal(parse_formula("C2H6"), {"C": 2, "H": 6})
assert_equal(parse_formula("H2O(g)"), {"H": 2, "O": 1})
assert_equal(parse_formula("Fe2O3"), {"Fe": 2, "O": 3})
assert_equal(raises_value_error(parse_formula, "h2o"), True)
assert_equal(raises_value_error(parse_formula, ""), True)

# ---------- balance_equation ----------
assert_equal(balance_equation(["CH4", "O2"], ["CO2", "H2O"]),
             ({"CH4": 1, "O2": 2}, {"CO2": 1, "H2O": 2}))
assert_equal(balance_equation(["C3H8", "O2"], ["CO2", "H2O"]),
             ({"C3H8": 1, "O2": 5}, {"CO2": 3, "H2O": 4}))
assert_equal(balance_equation(["H2", "O2"], ["H2O"]),
             ({"H2": 2, "O2": 1}, {"H2O": 2}))
assert_equal(balance_equation(["Fe", "O2"], ["Fe2O3"]),
             ({"Fe": 4, "O2": 3}, {"Fe2O3": 2}))
assert_equal(raises_value_error(balance_equation, ["CH4"], ["CO2"]), True)
