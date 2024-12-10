# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides GUI based easy to use approach to perform various sophisticated chemical operations/calculations.
# This file creates interface for Weight to Weight Ration calculation operation on chemical compounds.

from tkinter import *
import customtkinter
from customtkinter import CTkLabel, CTkOptionMenu
from pasta.base.fstring_utils import placeholder
from tkinter import ttk
from customtkinter import CTkLabel, CTkOptionMenu
from pasta.base.fstring_utils import placeholder
from ttkwidgets.autocomplete import AutocompleteCombobox
import weightPerWeight as ww
import database as db
from weightPerWeight import WeightPerWeight
import pymysql

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

def connectDB():
    """
    A function to connect to the database and return the connection object.
    """
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Chemistry.123',
        database='ChemicalDatabase',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


def fetchChemicalNames(cursor):
    """A function that fetches chemical names from the database Compound and returns the chemical names."""

    cursor.execute("SELECT ChemicalName FROM compounds")
    result = cursor.fetchall()
    names = [row['ChemicalName'] for row in result]
    return names


def fetchChemicalFormulas(cursor, cName):
    """A function that fetch chemical formula of the compound from the compound database."""

    cursor.execute("SELECT ChemicalFormula FROM compounds where ChemicalName = %s",(cName,))
    result = cursor.fetchone()
    if result:
        return result['ChemicalFormula']
    return ""

def tabWWSolutions(tabN, lbl):
    """ This function that creates an interface with necessary widgets for Weight to weight ratio tab widget."""

    def populateChemicalNames():
        """This function populates the comboboxes for compound A, B and Product C,D. with the chemical names of compound."""

        connection = connectDB()
        cursor = connection.cursor()
        chemical_names = fetchChemicalNames(cursor)
        cboCompoundA['completevalues'] = chemical_names
        cursor.close()
        connection.close()

    def on_select(event):
        """This function loads the chemical formula and molecular weight in their respective widgets based on chemical
         name selected for compound A."""

        selected_name = cboCompoundA.get()
        if selected_name:
            connection = connectDB()
            cursor = connection.cursor()
            chemical_formula = fetchChemicalFormulas(cursor, selected_name)
            cboCompoundAF.set(chemical_formula)
            cursor.close()
            connection.close()

    def clearFields():
        """Resets combobox and textboxes"""
        txtCompoundAWeight.delete(0, END)
        txtPercentage.delete(0, END)
        txtSolventAWeight.delete(0, END)

        cboCompoundA.set('')
        cboCompoundAF.set('')

    def calculateWW():
        """This function performs calculation for weight to volume operation on user input."""

        calculator = WeightPerWeight()
        try:
            # input compound weights and units.
            compoundAW = txtCompoundAWeight.get().strip()
            compoundAW = float(compoundAW) if compoundAW else None
            compoundAU = cboCompoundAUnits.get().strip()

            compoundBW = txtSolventAWeight.get().strip()
            compoundBW = float(compoundBW) if compoundBW else None
            compoundBU = cboSolventAWeightUnits.get().strip()

            percentSolution = txtPercentage.get().strip()
            percentSolution = float(percentSolution) if percentSolution else None

            # Convert all weight to grams
            compoundA = calculator.convert_to_grams(compoundAW, compoundAU) if compoundAW and compoundAU else None
            compoundB = calculator.convert_to_grams(compoundBW, compoundBU) if compoundBW and compoundBU else None

            # Calculate the fourth value that was left blank
            result = calculator.compute_solution(compoundA, compoundB, percentSolution)

            if compoundA is None:
                result = f"The weight of Compound A needed is: {result:.2f} grams."
            elif compoundB is None:
                result = f"The weight of Compound B needed is: {result:.2f} grams."
            elif percentSolution is None:
                result = f"The percent solution is: {result:.2f}%."
            else:
                result = "Error: All inputs provided, but one should be left blank."
            lblOutput.configure(text=result)

        except Exception as e:
            lblOutput.configure(text=f"An error occurred: {e}")

        clearFields()

    # Tab Title
    lblTitle = customtkinter.CTkLabel(tabN, text=lbl, font=("Helvetica", 20), fg_color="#1a75ff", width=900, height=35,
                                      text_color="#404040")
    lblTitle.pack()

    # Compound A
    lblCompoundA = customtkinter.CTkLabel(tabN, text="Choose the Compound", width=200, font=("Helvetica", 15))
    lblCompoundA.pack()
    cboCompoundA = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundA.pack()
    cboCompoundA.bind("<<ComboboxSelected>>", on_select)
    populateChemicalNames()

    lblCompoundAF = customtkinter.CTkLabel(tabN, text="Compound Formula", width=200, font=("Helvetica", 15))
    lblCompoundAF.pack()
    cboCompoundAF = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundAF.pack()

    lblCompoundAWeight = customtkinter.CTkLabel(tabN, text="Compound A Weight", font=("Helvetica", 15))
    lblCompoundAWeight.pack()
    txtCompoundAWeight = customtkinter.CTkEntry(tabN, width=300,border_color="#1a75ff")
    txtCompoundAWeight.pack()

    lblCompoundAUnits = customtkinter.CTkLabel(tabN, text="Units", width=300, font=("Helvetica", 15))
    lblCompoundAUnits.pack()
    cboCompoundAUnits = customtkinter.CTkOptionMenu(tabN, values=["Kilogram", "Gram", "Milligram"], width=300,
                                                    dropdown_font=("Helvetica", 19))
    cboCompoundAUnits.pack()

    lblSolventAWeight = customtkinter.CTkLabel(tabN, text="Weight of Solvent A", font=("Helvetica", 15))
    lblSolventAWeight.pack()
    txtSolventAWeight = customtkinter.CTkEntry(tabN, width=300,border_color="#1a75ff")
    txtSolventAWeight.pack()

    lblSolventAWeightUnits = customtkinter.CTkLabel(tabN, text="Units", font=("Helvetica", 15))
    lblSolventAWeightUnits.pack()
    cboSolventAWeightUnits = customtkinter.CTkOptionMenu(tabN, values=["Kilogram", "Gram", "Milligram"], width=300,
                                                    dropdown_font=("Helvetica", 19))
    cboSolventAWeightUnits.pack()

    lblPercentage = customtkinter.CTkLabel(tabN, text="Percentage of Solution (%)", font=("Helvetica", 15))
    lblPercentage.pack()
    txtPercentage = customtkinter.CTkEntry(tabN, width=300,border_color="#1a75ff")
    txtPercentage.pack()

    # Button to perform Weight to weight Ratio operation
    btnCalculate = customtkinter.CTkButton(tabN, text="Calculate",font=("Helvetica",15), width=300,command = calculateWW)
    btnCalculate.pack(pady=25)

    # Output Label
    lblOutput = customtkinter.CTkLabel(tabN, text="Output", font = ("Helvetica",15),fg_color="#1a75ff", width=800, height=35, text_color="#262626")
    lblOutput.pack()
