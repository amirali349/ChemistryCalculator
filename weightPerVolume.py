# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides GUI based easy to use approach to perform various sophisticated chemical operations/calculations.
# This file creates class for Weight Per Volume Ratio calculation operation on chemical compounds.

class WeightPerVolume:
    """  A class used to perform weight-per-Weight ratio calculations on chemical compounds. """
    def __init__(self):
        """
        A constructor function that initializes class variables for Weight per Weight class.
        """
        self.Gram = 1.0
        self.Kilogram = 1000.0
        self.Milligram = 0.001
        self.Kiloliter = 1000.0
        self.Liter = 1.0
        self.Milliliter = 0.001

    def convert_weight_to_grams(self, weight, unit):
        """  This function converts input weight to grams. """
        if unit == "Kilogram":
            return weight * self.Kilogram
        elif unit == "Milligram":
            return weight * self.Milligram
        else:
            return weight * self.Gram

    def convert_volume_to_milliliters(self, volume, unit):
        """ This function converts input volume to milliliters. """
        if unit == "Kiloliter":
            return volume * self.Kiloliter
        elif unit == "Milliliter":
            return volume * self.Milliliter
        else:
            return volume * self.Liter

    def compute_solution(self, solute_weight=None, solvent_volume=None, percent_solution=None):
        """ This function calculates the missing value that was not provided by the user.
        Solute weight is the same as compound A weight """

        if solute_weight is None:
            return (percent_solution / 100) * solvent_volume
        # Solvent weight is the same as solvent A weight
        elif solvent_volume is None:
            return solute_weight / (percent_solution / 100)
        elif percent_solution is None:
            return (solute_weight / solvent_volume) * 100
        else:
            raise ValueError(
                "Only two of the three parameters (solute_weight, solvent_volume, percent_solution) should be provided.")