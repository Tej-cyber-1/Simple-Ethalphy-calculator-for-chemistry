# ============================================================
# PASTE THIS INTO main.py, right ABOVE the line: start_server(State())
# You can choose to use all unit tests or none at all 
#( I just put these many to get the project requirements)
# ============================================================
from bakery import assert_equal


def sample_reaction(delta_h_kj: float = -890.5) -> Reaction:
    """Build a Reaction for tests. (Test helper, not a route.)"""
    return Reaction("1 CH4 + 2 O2 → 1 CO2 + 2 H2O", delta_h_kj, ["CH4", "O2"])


# ---------- helper function tests ----------
assert_equal(convert(10.0, "kJ"), 10.0)
assert_equal(round(convert(418.4, "kcal"), 2), 100.0)
assert_equal(format_side({"CH4": 1, "O2": 2}), "1 CH4 + 2 O2")
assert_equal(history_labels(State()), [])
assert_equal(history_labels(State(history=[sample_reaction()])),
             ["1: 1 CH4 + 2 O2 → 1 CO2 + 2 H2O"])
assert_equal(len(nav()), 4)

# ---------- index ----------
assert_equal(index(State()).state.result, "")
assert_equal(index(State(result="hello")).content[-1], "hello")

# ---------- calculate ----------
good_state = State()
calculate(good_state, "CH4", "O2", "CO2", "H2O")
assert_equal(len(good_state.history), 1)
assert_equal(good_state.history[0].equation, "1 CH4 + 2 O2 → 1 CO2 + 2 H2O")
assert_equal(round(good_state.history[0].delta_h_kj, 2), -890.5)
assert_equal(good_state.reactant1, "CH4")

empty_state = State()
calculate(empty_state, "", "", "CO2", "")
assert_equal(empty_state.result, "Enter at least one reactant and one product.")
assert_equal(empty_state.history, [])

unknown_state = State()
calculate(unknown_state, "Xyz", "", "CO2", "")
assert_equal(unknown_state.result.startswith("Error:"), True)
assert_equal(unknown_state.history, [])

unbalanced_state = State()
calculate(unbalanced_state, "CH4", "", "CO2", "")
assert_equal(unbalanced_state.result.startswith("Error:"), True)
assert_equal(unbalanced_state.history, [])

# ---------- result_page ----------
exo_state = State(history=[sample_reaction(-890.5)])
exo_page = result_page(exo_state)
assert_equal("Exothermic (releases heat)" in exo_page.content, True)
assert_equal(exo_state.result, "Last: 1 CH4 + 2 O2 → 1 CO2 + 2 H2O | ΔH° = -890.50 kJ")

endo_page = result_page(State(history=[sample_reaction(52.4)]))
assert_equal("Endothermic (absorbs heat)" in endo_page.content, True)

neutral_page = result_page(State(history=[sample_reaction(0.0)]))
assert_equal("Thermoneutral" in neutral_page.content, True)

# ---------- history_page ----------
assert_equal("No calculations yet." in history_page(State()).content, True)

both_state = State(history=[sample_reaction(-890.5), sample_reaction(52.4)])
both_text = "Showing 2 reaction(s), summed ΔH: -838.10 kJ"
assert_equal(both_text in history_page(both_state).content, True)

filtered_state = State(history=[sample_reaction(-890.5), sample_reaction(52.4)],
                       only_exothermic=True)
filtered_text = "Showing 1 reaction(s), summed ΔH: -890.50 kJ"
assert_equal(filtered_text in history_page(filtered_state).content, True)

# ---------- apply_filter ----------
filter_state = State()
apply_filter(filter_state, True)
assert_equal(filter_state.only_exothermic, True)

# ---------- detail_page ----------
detail = detail_page(State(history=[sample_reaction()]), "1: anything")
assert_equal("Compounds: CH4, O2" in detail.content, True)
assert_equal("ΔHf° CH4: -74.60 kJ/mol" in detail.content, True)

# ---------- delete_reaction ----------
delete_state = State(history=[sample_reaction(-890.5), sample_reaction(52.4)])
delete_reaction(delete_state, "1: anything")
assert_equal(len(delete_state.history), 1)
assert_equal(delete_state.history[0].delta_h_kj, 52.4)

# ---------- clear_history ----------
clear_state = State(history=[sample_reaction()], result="old result")
clear_history(clear_state)
assert_equal(clear_state.history, [])
assert_equal(clear_state.result, "")

# ---------- settings_page / save_settings ----------
assert_equal(settings_page(State()).state.unit, "kJ")
unit_state = State()
save_settings(unit_state, "kcal")
assert_equal(unit_state.unit, "kcal")

# ---------- help_page ----------
help_state = State()
assert_equal(help_page(help_state).state, help_state)
