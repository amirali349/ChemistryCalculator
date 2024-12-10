# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides GUI based easy to use approach to perform various sophisticated chemical operations/calculations.
# This file creates interface for Dilution operation on chemical compounds.

from tkinter import *
import customtkinter
from customtkinter import CTkLabel, CTkOptionMenu
from ttkwidgets.autocomplete import AutocompleteCombobox
import dilution as di
import database as db

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


def tabDilution(tabN, lbl):
    """ This function that creates an interface with necessary widgets for Dilution widget."""

    def calculateDilution():
        """This function performs calculation for dilution operation on user input."""

        calculator = di.DilutionCalculator() # Initializing DilutionCalculator class object
        try:
            # Assigning inputs to the variables from widgets
            concA = txtCompoundAConcentration.get().strip()
            concB = txtCompoundBConcentration.get().strip()
            volA = txtCompoundAVolume.get().strip()
            volB = txtCompoundBVolume.get().strip()
            volAUnit = cboCompoundAUnits.get().strip()
            volBUnit = cboCompoundBUnits.get().strip()

            concA = float(concA) if concA else None
            concB = float(concB) if concB else None
            volAValue = float(volA) if volA else None
            volBValue = float(volB) if volB else None

            # Converting the volume to milliters and assign it to variables
            volA = calculator.convert_volume_to_milliliters(volAValue, volAUnit) if volAValue else None
            volB = calculator.convert_volume_to_milliliters(volBValue, volBUnit) if volBValue else None

            result = calculator.compute_missing_value(concA, concB, volA, volB)

            if concA is None:
                result = f"The concentration of Compound A is: {result:.2f}%."
            elif concB is None:
                result = f"The concentration of Compound B is: {result:.2f}%."
            elif volA is None:
                result = f"The volume of Compound A is: {result:.2f} mL."
            elif volB is None:
                result = f"The volume of Compound B is: {result:.2f} mL."
            else:
                result = "Error: All inputs provided, but one should be left blank."
            lblOutput.configure(text=result)
        except Exception as e:
            lblOutput.configure(text=f"An error occurred: {e}")

    # Title
    lblTitle = customtkinter.CTkLabel(tabN, text=lbl, font=("Helvetica", 20), fg_color="#1a75ff", height=35, width=900,
                                      text_color="#404040")
    lblTitle.pack(pady=5)

    lblPrompt = customtkinter.CTkLabel(tabN, text="Please enter any three of the following: ", text_color="#404040",
                                       width=500, font=("Helvetica", 15), fg_color="#1a75ff")
    lblPrompt.pack(pady=5)

    # Compound A widgets
    lblCompoundAConcentration = customtkinter.CTkLabel(tabN, text="Concentration of Compound A (%): ",
                                                       font=("Helvetica", 15), width=250, anchor="e")
    lblCompoundAConcentration.pack(pady=5)
    txtCompoundAConcentration = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtCompoundAConcentration.pack(pady=5)

    lblCompoundAVolume = customtkinter.CTkLabel(tabN, text="Volume of Compound A: ", font=("Helvetica", 15), width=250)
    lblCompoundAVolume.pack(pady=5)
    txtCompoundAVolume = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtCompoundAVolume.pack(pady=5)

    lblCompoundAUnits = customtkinter.CTkLabel(tabN, text="Units: ", font=("Helvetica", 15), width=80)
    lblCompoundAUnits.pack(pady=5)
    cboCompoundAUnits = customtkinter.CTkOptionMenu(tabN, values=["Kiloliter", "Liter", "Milliliter"], width=300,
                                                    dropdown_font=("Helvetica", 19))
    cboCompoundAUnits.pack(pady=5)

    # Compound B widgets
    lblCompoundBConcentration = customtkinter.CTkLabel(tabN, text="Concentration of Compound B (%): ",
                                                       font=("Helvetica", 15), width=250, anchor="e")
    lblCompoundBConcentration.pack(pady=5)
    txtCompoundBConcentration = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtCompoundBConcentration.pack(pady=5)

    lblCompoundBVolume = customtkinter.CTkLabel(tabN, text="Volume of Compound B: ", font=("Helvetica", 15), width=250)
    lblCompoundBVolume.pack(pady=5)
    txtCompoundBVolume = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtCompoundBVolume.pack(pady=5)

    lblCompoundBUnits = customtkinter.CTkLabel(tabN, text="Units: ", font=("Helvetica", 15), width=80)
    lblCompoundBUnits.pack(pady=5)
    cboCompoundBUnits = customtkinter.CTkOptionMenu(tabN, values=["Kiloliter", "Liter", "Milliliter"], width=300,
                                                    dropdown_font=("Helvetica", 19))
    cboCompoundBUnits.pack(pady=5)

    # Button to perform Expect Yield Module operation
    btnCalculate = customtkinter.CTkButton(tabN, text="Calculate", font=("Helvetica", 15), width=250,
                                           command=calculateDilution)
    btnCalculate.pack(pady=15)

    # Output Label
    lblOutput = customtkinter.CTkLabel(tabN, text="Output", font=("Helvetica", 20), fg_color="#1a75ff",
                                       height=35, width=800, text_color="#404040")
    lblOutput.pack(pady=5)
