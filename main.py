from drafter import *
from dataclasses import dataclass, field
from backend import get_species_data, balance_equation


# Global CONSTANT (allowed): 1 kcal = 4.184 kJ
KJ_PER_KCAL = 4.184

set_website_title("ThermoStats")
set_site_information(
    author="Tej Shourya Boppana",
    description="Simple ethalphy calculator for chem-engineers built by chem-engineer",
    sources="Thanks to the Drafter docs.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/Tej-cyber-1/Simple-Ethalphy-calculator-for-chemistry"]
)
hide_debug_information()

set_website_framed(False)
@dataclass
class Reaction:
    """One saved calculation."""
    equation: str
    delta_h_kj: float          # stored in kJ; converted when displayed
    species: list[str]         # every compound involved


@dataclass
class State:
    reactant1: str = ""
    reactant2: str = ""
    product1: str = ""
    product2: str = ""
    result: str = ""
    unit: str = "kJ"
    only_exothermic: bool = False
    history: list[Reaction] = field(default_factory=list)


#helper functions

def convert(delta_h_kj: float, unit: str) -> float:
    """Convert a kJ --> user's chosen unit."""
    if unit == "kcal":
        return delta_h_kj / KJ_PER_KCAL
    return delta_h_kj


def format_side(side: dict) -> str:
    """Turn {'CH4': 1, 'O2': 2} --> '1 CH4 + 2 O2'."""
    parts = []
    for name, coeff in side.items():
        parts.append(f"{coeff} {name}")
    return " + ".join(parts)


def nav() -> list:
    """Navigation buttons shown on every page."""
    return [
        Button("Calculator", index),
        Button("History", history_page),
        Button("Settings", settings_page),
        Button("Help", help_page),
    ]


def history_labels(state: State) -> list[str]:
    """Labels like '1: CH4 + 2 O2 -> ' used by the SelectBox."""
    labels = []
    for i, rxn in enumerate(state.history):
        labels.append(f"{i + 1}: {rxn.equation}")
    return labels


#routes 
@route
def index(state: State) -> Page:
    content = [
        Header("🔥 Thermo-We Got The Heat Calculator 🔥"),
        *nav(),
        "Enter plain formulas like CH4, O2, CO2, H2O. Leave 2nd boxes empty if unused.",
        "Reactant 1:", TextBox("reactant1", state.reactant1),
        "Reactant 2:", TextBox("reactant2", state.reactant2),
        "Product 1:", TextBox("product1", state.product1),
        "Product 2:", TextBox("product2", state.product2),
        Button("Calculate Enthalpy", calculate),
    ]
    if state.result:
        content.append(state.result)
    return Page(state, content)


@route
def calculate(state: State, reactant1: str, reactant2: str,
              product1: str, product2: str) -> Page:
    state.reactant1, state.reactant2 = reactant1, reactant2
    state.product1, state.product2 = product1, product2

    reactants = [c.strip() for c in (reactant1, reactant2) if c.strip()]
    products = [c.strip() for c in (product1, product2) if c.strip()]

    if not reactants or not products:
        state.result = "Enter at least one reactant and one product."
        return index(state)

    try:
        # Our own balancer (backend.py) returns whole-number coefficients.
        reac, prod = balance_equation(reactants, products)
        #Hess's law: sum(n * dHf products) - sum(n * dHf reactants)
        h_prod = sum(n * get_species_data(s) for s, n in prod.items())
        h_reac = sum(n * get_species_data(s) for s, n in reac.items())
        delta_h = h_prod - h_reac
    except Exception as error:
        state.result = f"Error: {error}"
        return index(state)

    equation = f"{format_side(reac)} → {format_side(prod)}"
    state.history.append(Reaction(equation, delta_h, reactants + products))
    return result_page(state)


@route
def result_page(state: State) -> Page:
    rxn = state.history[-1]
    shown = convert(rxn.delta_h_kj, state.unit)
    if rxn.delta_h_kj < 0:
        kind = "Exothermic (releases heat)"
    elif rxn.delta_h_kj > 0:
        kind = "Endothermic (absorbs heat)"
    else:
        kind = "Thermoneutral"
    state.result = f"Last: {rxn.equation} | ΔH° = {shown:.2f} {state.unit}"
    return Page(state, [
        Header("Result"),
        *nav(),
        f"Balanced: {rxn.equation}",
        f"ΔH°rxn = {shown:.2f} {state.unit}",
        kind,
    ])


@route
def history_page(state: State) -> Page:
    content = [Header("History"), *nav()]
    if not state.history:
        content.append("No calculations yet.")
        return Page(state, content)

    content.append("Only show exothermic reactions:")
    content.append(CheckBox("only_exothermic", state.only_exothermic))
    content.append(Button("Apply filter", apply_filter))

    total = 0.0
    shown_count = 0
    for rxn in state.history:  # loop over instance attributes
        if state.only_exothermic and rxn.delta_h_kj >= 0:
            continue
        value = convert(rxn.delta_h_kj, state.unit)
        content.append(f"{rxn.equation}  →  {value:.2f} {state.unit}")
        total += value
        shown_count += 1
    content.append(f"Showing {shown_count} reaction(s), summed ΔH: {total:.2f} {state.unit}")

    content.append("Pick a saved reaction:")
    content.append(SelectBox("choice", history_labels(state), history_labels(state)[0]))
    content.append(Button("View details", detail_page))
    content.append(Button("Delete", delete_reaction))
    content.append(Button("Clear all", clear_history))
    return Page(state, content)


@route
def apply_filter(state: State, only_exothermic: bool) -> Page:
    state.only_exothermic = only_exothermic
    return history_page(state)


@route
def detail_page(state: State, choice: str) -> Page:
    index_chosen = int(choice.split(":")[0]) - 1
    rxn = state.history[index_chosen]
    lines = [f"Compounds: {', '.join(rxn.species)}"]
    for name in rxn.species:
        lines.append(f"ΔHf° {name}: {convert(get_species_data(name), state.unit):.2f} {state.unit}/mol")
    return Page(state, [
        Header("Reaction Details"), *nav(),
        rxn.equation,
        f"ΔH°rxn = {convert(rxn.delta_h_kj, state.unit):.2f} {state.unit}",
        *lines,
    ])


@route
def delete_reaction(state: State, choice: str) -> Page:
    index_chosen = int(choice.split(":")[0]) - 1
    state.history.pop(index_chosen)
    return history_page(state)


@route
def clear_history(state: State) -> Page:
    state.history = []
    state.result = ""
    return history_page(state)


@route
def settings_page(state: State) -> Page:
    return Page(state, [
        Header("Settings"), *nav(),
        "Display units:",
        SelectBox("unit", ["kJ", "kcal"], state.unit),
        Button("Save", save_settings),
    ])


@route
def save_settings(state: State, unit: str) -> Page:
    state.unit = unit
    return settings_page(state)


@route
def help_page(state: State) -> Page:
    return Page(state, [
        Header("Help"), *nav(),
        "Enter one or two reactants and one or two products as plain formulas (H2O, not 'water').",
        "The equation is balanced automatically, and standard enthalpies of formation come from a built-in table.",
        "ΔH°rxn = Σ n·ΔHf°(products) − Σ n·ΔHf°(reactants).",
        "Negative = exothermic, positive = endothermic.",
    ])


start_server(State())
