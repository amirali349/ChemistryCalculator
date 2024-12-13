# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides GUI based easy to use approach to perform various sophisticated chemical operations/calculations.
# This file creates class for Limiting Reactant calculation operation on chemical compounds.

class LimitingReactant:
    def __init__(self, compound_a, weight_a, unit_a, coeff_a, compound_b, weight_b, unit_b, coeff_b, molar_mass_a, molar_mass_b):
        # Initialize variables
        self.compound_a = compound_a
        self.weight_a = weight_a
        self.unit_a = unit_a
        self.coeff_a = coeff_a
        self.compound_b = compound_b
        self.weight_b = weight_b
        self.unit_b = unit_b
        self.coeff_b = coeff_b
        self.molar_mass_a = molar_mass_a
        self.molar_mass_b = molar_mass_b
        """ This is the value in the third column in the database Labeled "Molecular weight"
         value has units of g/mol and needs to be found when a person inputs the compound.
         Below is a test case where I hard coded a few test values. """
        #self.molar_masses = {

        #    'CH4': 16.04,
        #    'O₂': 32.00,
        #    'CO2': 44.01,
        #    'H2O': 18.02,
        #    'N₂': 28.0,
        #    'H₂': 2.02,
        #    'NH3': 17.0,
        #    'C6H12O6': 180.06
        #}
        self.limiting_reactant = None
        self.expected_yield = None

    #def get_molar_mass(self, compound):
        # Looks for the key and returns the appropriate molecular weight value
        # Used before database was properly setup
        #return self.molar_masses.get(compound, None)

    def convert_to_grams(self, weight, unit):
        # Ensures that all calculations are done in grams regardless of the units they entered
        conversion_factors = {
            'Milligram': 0.001,
            'Gram': 1,
            'Kilogram': 1000
        }
        return weight * conversion_factors[unit]

    def calculate_moles(self, weight_g, molar_mass):
        # Calculation for moles of a compound. Take the weight entered for compound A divided by
        # the molecular weight for compound A.
        return weight_g / molar_mass

    def find_limiting_reactant(self):


        # Convert weights to grams
        weight_a_g = self.convert_to_grams(self.weight_a, self.unit_a)
        weight_b_g = self.convert_to_grams(self.weight_b, self.unit_b)

        # Get molar masses
        #molar_mass_a = self.get_molar_mass(self.compound_a)
        #molar_mass_b = self.get_molar_mass(self.compound_b)
        # Set molar masses from database
        molar_mass_a = self.molar_mass_a
        molar_mass_b = self.molar_mass_b

        if molar_mass_a is None or molar_mass_b is None:
            raise ValueError("Molar mass of one or both compounds is not available.")

        # Calculate moles
        moles_a = self.calculate_moles(weight_a_g, molar_mass_a)
        moles_b = self.calculate_moles(weight_b_g, molar_mass_b)

        # Determine limiting reactant
        # This calculates a molar value for compound A and compound B based off the weight given
        # and the ratio of the two coefficients.
        moles_used_reactant_a = moles_a * (self.coeff_b / self.coeff_a)
        moles_used_reactant_b = moles_b * (self.coeff_a / self.coeff_b)

        # Compare the two molar values computed for compounds A and B to the mole values of B and A
        # If one has less than what is currently available that is the limiting reactant
        # and the reaction cannot consume anymore material
        if moles_used_reactant_b > moles_a:
            self.limiting_reactant = self.compound_a
        elif moles_used_reactant_a > moles_b:
            self.limiting_reactant = self.compound_b
        else:
            self.limiting_reactant = None

        return self.limiting_reactant


