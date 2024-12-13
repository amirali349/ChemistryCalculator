# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides GUI based easy to use approach to perform various sophisticated chemical operations/calculations.
# This file creates class for Stoichiometry calculation operation on chemical compounds.

import math
from sympy import Eq, symbols, solve
from fractions import Fraction
from collections import defaultdict

class ChemicalEquationBalancer:
    def __init__(self, compound_a, compound_b, product_c, product_d):
        """
        This is a constructor function that initializes the class variables.
        :param compound_a: Compound A
        :param compound_b: Compound B
        :param product_c: Product C
        :param product_d: Product D
        """
        self.compound_a = compound_a
        self.compound_b = compound_b
        self.product_c = product_c
        self.product_d = product_d
        self.a, self.b, self.c, self.d = symbols('a b c d')

    def parse_formula(self, formula):
        """ This function takes the chemical formula and parse it to identify its chemical elements and coefficients."""

        # Define a dictionary to map subscript characters to regular digits
        subscript_map = {
            '₀': '0', '₁': '1', '₂': '2', '₃': '3', '₄': '4', '₅': '5',
            '₆': '6', '₇': '7', '₈': '8', '₉': '9'
        }
        # Replace subscript characters with regular digits
        for sub, normal in subscript_map.items():
            formula = formula.replace(sub, normal)

        elements = {}
        stack = []  # To handle nested parentheses
        i = 0

        while i < len(formula):
            # This accounts for cases such as Ca(OH)2
            if formula[i] == '(':
                # Start of a group
                stack.append(elements)
                elements = {}
                i += 1
            elif formula[i] == ')':
                # End of a group
                i += 1
                multiplier = 0
                while i < len(formula) and formula[i].isdigit():
                    multiplier = multiplier * 10 + int(formula[i])
                    i += 1
                multiplier = multiplier if multiplier > 0 else 1
                for element, count in elements.items():
                    elements[element] = count * multiplier
                parent_elements = stack.pop()
                for element, count in elements.items():
                    if element in parent_elements:
                        parent_elements[element] += count
                    else:
                        parent_elements[element] = count
                elements = parent_elements
            else:
                # Regular element and count parsing
                if i + 1 < len(formula) and formula[i + 1].islower():
                    element = formula[i:i + 2]
                    i += 2
                else:
                    element = formula[i]
                    i += 1

                count = 0
                while i < len(formula) and formula[i].isdigit():
                    count = count * 10 + int(formula[i])
                    i += 1
                count = count if count > 0 else 1

                if element in elements:
                    elements[element] += count
                else:
                    elements[element] = count

        return elements

    def combine_counts(self, *compound_dicts):
        """This function combines multiple dictionaries of element counts into a single dictionary."""

        # Count the number of elements on each side. E.g 1 'C' in CH4; 2 'O' in O2
        total_counts = {}
        for compound in compound_dicts:
            for element, count in compound.items():
                if element in total_counts:
                    total_counts[element] += count
                else:
                    total_counts[element] = count
        return total_counts

    def solve_linear_system(self, equations, a_guess):
        """This function solves a system of linear equations with a given initial guess."""

        # Define coefficient variables
        a, b, c, d = symbols('a b c d')

        solution_ordered = {}

        # Set the guessed value for 'a' so that equations can be solved
        equations = [eq.subs(a, a_guess) for eq in equations]

        # Solve the system of equations
        solution = solve(equations, [b, c, d])

        # If the solution is a list, just pick the first solution (if any)
        if isinstance(solution, list):
            if len(solution) > 0:
                solution = solution[0]  # Use the first solution
            else:
                solution = {}  # Empty solution in case of no solutions

        # Reordered so that guessed value of 'a' is added to the solution and comes first
        solution_ordered[a] = a_guess
        for var in [b, c, d]:
            solution_ordered[var] = solution.get(var, 0)  # Default to 0 if variable not found

        denominators = {}
        for var, value in solution_ordered.items():
            # Check if value is None
            if value is not None:
                # Convert float to Fraction for consistent denominator extraction
                if isinstance(value, float):
                    value = Fraction(value).limit_denominator()  # Converts float to Fraction
                denominators[var] = value.denominator
            else:
                denominators[var] = 1  # Assign a default denominator for None (or handle as needed)

        # Compute the least common multiple of the denominators
        lcm_value = math.lcm(*denominators.values())

        # Scale all values to make them whole integers
        scaled_solution = {var: int(value * lcm_value) if value is not None else 0 for var, value in
                           solution_ordered.items()}

        return scaled_solution

    def balance_equation(self, counts_a, counts_b, counts_c, counts_d):
        """This function balances the equation."""
        # Coefficient symbols
        a, b, c, d = symbols('a b c d')

        # Modify the counts of each input to match the value e.g: {'C': a, 'H': 4*a}
        counts_a_modified = self.multiply_counts(counts_a, a)
        counts_b_modified = self.multiply_counts(counts_b, b)
        counts_c_modified = self.multiply_counts(counts_c, c)
        counts_d_modified = self.multiply_counts(counts_d, d)

        # Combine counts dictionaries into a structured format
        lhs_dicts = [counts_a_modified, counts_b_modified]  # Left-hand side: counts_a and counts_b
        rhs_dicts = [counts_c_modified, counts_d_modified]  # Right-hand side: counts_c and counts_d

        # Group Terms by their Letter: e.g 'C'
        def combine_counts(dicts):
            combined = defaultdict(list)
            for counts in dicts:
                for letter, term in counts.items():
                    combined[letter].append(term)
            return combined

        # Combine terms for LHS and RHS of equation
        lhs_combined = combine_counts(lhs_dicts)
        rhs_combined = combine_counts(rhs_dicts)

        # Generate equations by combining LHS and RHS terms
        equations = []
        for letter in set(lhs_combined.keys()).union(rhs_combined.keys()):
            # Needs to be converted to string
            lhs_terms = " + ".join(map(str, lhs_combined[letter])) if letter in lhs_combined else "0"
            rhs_terms = " + ".join(map(str, rhs_combined[letter])) if letter in rhs_combined else "0"
            equations.append(f"{letter}: {lhs_terms} = {rhs_terms}")

        # Generate the List of Linear Equations
        linear_equations = []

        for eq_str in equations:
            # Needs to be converted back into a sympy equation
            _, equation = eq_str.split(": ")  # Split to isolate the equation part from letter
            lhs, rhs = equation.split(" = ")  # Split into LHS and RHS
            lhs_expr = eval(lhs)  # Convert LHS to a sympy expression
            rhs_expr = eval(rhs)  # Convert RHS to a sympy expression
            linear_equations.append(Eq(lhs_expr, rhs_expr))  # Create a sympy equation

        # Pass equations into the solve linear equation function. A guess of 1 allows a solution to be found
        coefficients = self.solve_linear_system(linear_equations, a_guess=1)

        #print(solution)
        return(coefficients)


    def multiply_counts(self, counts, factor):
        """This function multiplies the counts of each element in a dictionary by a given factor."""
        return {letter: factor * value for letter, value in counts.items()}

    def find_coefficients(self):
        """This function splits Compounds into Elements"""
        counts_a = self.parse_formula(self.compound_a)
        counts_b = self.parse_formula(self.compound_b)
        counts_c = self.parse_formula(self.product_c)
        # counts_d = self.parse_formula(product_d)
        # Ensures program works even if only three compounds are inputted.
        # E.g N2 + H2 = NH3.
        counts_d = self.parse_formula(self.product_d) if self.product_d else {}


        # Combine Element counts for the left and right sides
        left_counts = self.combine_counts(counts_a, counts_b)
        right_counts = self.combine_counts(counts_c, counts_d)

        # Check if the equation is balanced
        balanced = True
        for element in set(left_counts.keys()).union(right_counts.keys()):
            left_value = left_counts.get(element, 0)
            right_value = right_counts.get(element, 0)
            if left_value != right_value:
                balanced = False

        if balanced:
            return{self.a: 1, self.b: 1, self.c: 1, self.d: 1}
        else:
            # Balance the equation
            coefficients = self.balance_equation(counts_a, counts_b, counts_c, counts_d)
            return(coefficients)