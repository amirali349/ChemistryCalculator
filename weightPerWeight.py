# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides GUI based easy to use approach to perform various sophisticated chemical operations/calculations.
# This file creates class for Weight per Weight calculation operation on chemical compounds.

class WeightPerWeight:
    """
       A class used to perform weight-per-Weight ratio calculations on chemical compounds.
    """
    def __init__(self):
        """
        A constructor function that initializes class variables for Weight per volume class.
        """
        self.Gram = 1
        self.Milligram = 0.001
        self.Kilogram = 1000


    def convert_to_grams(self, weight, unit):
        """
        Convert input weight to grams
        :param weight: weight of compound
        :param unit: Unit of the weight
        :return: weight in grams
        """
        if unit == "Milligram":
            return weight * self.Milligram
        elif unit == "Kilogram":
            return weight * self.Kilogram
        else:
            return weight * self.Gram

    def compute_solution(self, compound_a=None, compound_b=None, percent_solution=None):
        """ Calculate the missing value that was not provided by the user. """
        if compound_a is None:
            return (percent_solution / 100) * compound_b
        elif compound_b is None:
            return compound_a / (percent_solution / 100)
        elif percent_solution is None:
            return (compound_a / compound_b) * 100
        else:
            raise ValueError(
                "Only two of the three parameters (compound_a, compound_b, percent_solution) should be provided.")