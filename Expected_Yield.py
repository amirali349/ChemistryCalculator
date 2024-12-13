# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides GUI based easy to use approach to perform various sophisticated chemical operations/calculations.
# This file creates class for Expected Yield Module calculation operation on chemical compounds.



class ExpectedYieldCalculator:
    """
           A class used to perform expected yield calculations on chemical compounds.
        """
    def __init__(self, compound_a, weight_a, unit_a, coeff_a, compound_b,
                 weight_b, unit_b, coeff_b, product_c, coeff_c, product_d, coeff_d,
                 molar_mass_a, molar_mass_b, molar_mass_c, molar_mass_d):
        # Initialize variables including product C and product D
        """
               A constructor function to initialize class variables.
                   compound_a : Name of the first reactant compound.
                   weight_a : Weight of the first reactant compound.
                   unit_a : Unit of the weight of the first reactant compound.
                   coeff_a : Coefficient of the first reactant in the balanced equation.
                   compound_b : Name of the second reactant compound.
                   weight_b : Weight of the second reactant compound.
                   unit_b : Unit of the weight of the second reactant compound.
                   coeff_b : Coefficient of the second reactant in the balanced equation.
                   product_c : Name of the first product compound.
                   coeff_c : Coefficient of the first product in the balanced equation.
                   product_d :Name of the second product compound.
                   coeff_d : Coefficient of the second product in the balanced equation.
                   molar_masses : Dictionary containing molar masses of some common compounds.
                   expected_yield_product_c : Expected yield of the first product.
                   expected_yield_product_d : float or None
               """
        self.compound_a = compound_a
        self.weight_a = weight_a
        self.unit_a = unit_a
        self.coeff_a = coeff_a
        self.compound_b = compound_b
        self.weight_b = weight_b
        self.unit_b = unit_b
        self.coeff_b = coeff_b
        self.product_c = product_c
        self.coeff_c = coeff_c
        self.product_d = product_d
        self.coeff_d = coeff_d
        self.molar_mass_a = molar_mass_a
        self.molar_mass_b = molar_mass_b
        self.molar_mass_c = molar_mass_c
        self.molar_mass_d = molar_mass_d
        # This is the value in the third column in the database Labeled "Molecular weight"
        # value has units of g/mol and needs to be found when a person inputs the compound.
        # Below is a test case where I hard coded a few test values.
        #self.molar_masses = {
        #    'CH4': 16.04,
        #    'O₂': 32.00,
        #    'CO₂': 44.01,
        #    'H₂O': 18.02,
        #    'H₂': 2.02,
        #    'NH₃': 17.0,
        #    'C6H12O6': 180.06
        #}
        # These will be our returned values
        self.expected_yield_product_c = None
        self.expected_yield_product_d = None

    #def get_molar_mass(self, compound):
     #   return self.molar_masses.get(compound, None)

    def convert_to_grams(self, weight, unit):
        """This function ensures that all calculations are done in grams regardless of the units they entered."""
        conversion_factors = {
            'Milligram': 0.001,
            'Gram': 1,
            'Kilogram': 1000
        }
        return weight * conversion_factors[unit]

    def calculate_moles(self, weight_g, molar_mass):
        """
                This function performs calculation for moles of a compound. Take the weight entered for compound A divided by
                the molecular weight for compound A.
                """
        # Calculation for moles of a compound. Take the weight entered for compound A divided by
        # the molecular weight for compound A.
        return weight_g / molar_mass

    def find_expected_yield(self):
        """
                 This function converts weight to grams.
                :param molarMassA: Molar mass of compound A.
                :param molarMassB: Molar mass of compound B.
                :param molarMassC: Molar mass of Product C.
                :param molarMassD: Molar mass of Product D.
                :return: expected_yield_product_c, self.expected_yield_product_d
                """
        # Convert weights to grams
        weight_a_g = self.convert_to_grams(self.weight_a, self.unit_a)
        weight_b_g = self.convert_to_grams(self.weight_b, self.unit_b)

        # Get molar masses
        #molar_mass_a = self.get_molar_mass(self.compound_a)
        #molar_mass_b = self.get_molar_mass(self.compound_b)
        #molar_mass_c = self.get_molar_mass(self.product_c)
        #molar_mass_d = self.get_molar_mass(self.product_d)

        molar_mass_a = self.molar_mass_a
        molar_mass_b = self.molar_mass_b
        molar_mass_c = self.molar_mass_c
        molar_mass_d = self.molar_mass_d

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

        # Calculates expected yield for product C. Takes the limiting reagent and multiplies by
        # the molar ratio (ratio of the proper coefficient) and again by the molar mass
        # of the product to get a final result in grams
        if moles_used_reactant_b > moles_a:
            self.expected_yield_product_c = moles_a * (self.coeff_c / self.coeff_a) * molar_mass_c
        elif moles_used_reactant_a > moles_b:
            self.expected_yield_product_c = moles_b * (self.coeff_c / self.coeff_b) * molar_mass_c
        else:
            self.expected_yield_product_c = None

        # Calculates expected yield for product D
        if self.coeff_d is not None and self.coeff_d != 0:
            if moles_used_reactant_b > moles_a:
                self.expected_yield_product_d = moles_a * (self.coeff_d / self.coeff_a) * molar_mass_d
            elif moles_used_reactant_a > moles_b:
                self.expected_yield_product_d = moles_b * (self.coeff_d / self.coeff_b) * molar_mass_d
            else:
                self.expected_yield_product_d = None
        else:
            self.expected_yield_product_d = 0

        return self.expected_yield_product_c, self.expected_yield_product_d