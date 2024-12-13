# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides a GUI-based, easy-to-use approach to perform various sophisticated chemical operations/calculations.
# This file creates a class for Dilution calculation operation on chemical compounds.

class DilutionCalculator:
    """
    A class used to perform dilution calculations on chemical compounds.
    """
    def __init__(self):
        """
        Constructor function that initializes all the necessary attributes for the DilutionCalculator object.
        """
        self.volume_units = {"Milliliter": 1, "Liter": 1000, "Kiloliter": 1000000}

    def convert_volume_to_milliliters(self, volume, unit):
        """
        A function that converts the given volume from the specified unit to milliliters.
        Parameters:
        volume : The volume to be converted.
        unit : The unit of the volume ('Milliliter', 'Liter', 'Kiloliter').
        Returns: The volume in milliliters.
        """
        if unit not in self.volume_units:
            raise ValueError(f"Unsupported volume unit '{unit}'. Use 'Milliliter', 'Liter', or 'Kiloliter'.")
        return volume * self.volume_units[unit]

    def compute_missing_value(self, conc_a=None, conc_b=None, vol_a=None, vol_b=None):
        """
        Computes the missing value (either concentration or volume) for the dilution calculation.
        Parameters
        conc_a: The initial concentration of the compound (default is None).
        conc_b: The final concentration of the compound (default is None).
        vol_a : The initial volume of the compound in milliliters (default is None).
        vol_b : The final volume of the compound in milliliters (default is None).
        Returns the computed missing value.
        """
        if conc_a is None:
            return (conc_b * vol_b) / vol_a
        elif conc_b is None:
            return (conc_a * vol_a) / vol_b
        elif vol_a is None:
            return (conc_b * vol_b) / conc_a
        elif vol_b is None:
            return (conc_a * vol_a) / conc_b
        else:
            raise ValueError("Only three of the four parameters (conc_a, conc_b, vol_a, vol_b) should be provided.")
