# Simple Chemical Reaction Enthalpy Calculator

A Python-based chemical reaction enthalpy calculator developed as a final project for **CISC106: Introduction to Computer Science for Engineers**, taught by Professor Wassil at the **University of Delaware** during Fall 2026.

## About the Project

ThermoStats is a simple chemistry calculator designed to help users calculate the standard enthalpy change (\(\Delta H^\circ\)) of chemical reactions.

The application takes chemical formulas for reactants and products, balances the chemical equation, and calculates the reaction's enthalpy change using Hess's Law.

The goal of this project was to apply introductory computer science concepts to a practical problem related to chemistry and chemical engineering.

## Features

- **Chemical Equation Balancing:** Automatically balances chemical reactions using a custom equation-balancing algorithm.
- **Enthalpy Calculations:** Calculates reaction enthalpy using standard enthalpies of formation and Hess's Law.
- **Reaction Classification:** Identifies reactions as exothermic, endothermic, or thermoneutral.
- **Unit Conversion:** Displays results in either kilojoules (kJ) or kilocalories (kcal).
- **Calculation History:** Saves previous calculations and allows users to review reaction details.
- **History Filtering:** Filter saved reactions to display only exothermic reactions.

## Technologies & Concepts

**Language:** Python

**Framework:** Drafter

**Programming Concepts:**
- Functions and modular programming
- Lists, dictionaries, and data structures
- Loops and conditional logic
- Regular expressions for chemical formula parsing
- Dataclasses for managing application state
- Exception handling and input validation
- Gaussian elimination and fraction-based arithmetic for balancing chemical equations

## How It Works

The calculator follows three main steps:

1. **Balance the Reaction:** The application parses chemical formulas and calculates the stoichiometric coefficients needed to balance the equation.
2. **Retrieve Enthalpy Values:** It retrieves the standard enthalpies of formation for the compounds from its built-in dataset.
3. **Calculate Reaction Enthalpy:** It applies Hess's Law

A negative result indicates an exothermic reaction, while a positive result indicates an endothermic reaction.

## Project Background

This project was developed as part of the Fall 2026 CISC106 course at the University of Delaware. It demonstrates how introductory programming techniques can be applied to scientific calculations and problems relevant to chemical engineering.

## Repository Contents

- `main.py` – Main application and user interface.
- `backend.py` – Chemical equation balancing, formula parsing, and enthalpy calculations.
- `unit_tests_main.py` – Tests for the main application.
- `unit_tests_backend.py` – Tests for backend calculations.
- `plan.pdf` – Initial project plan.
- `design.pdf` – Project design documentation.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.
