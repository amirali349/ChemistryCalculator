# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides GUI based easy to use approach to perform various sophisticated chemical operations/calculations.
# This file creates interface for Weight to Volume Ratio calculation operation on chemical compounds.


from tkinter import *
import customtkinter
from customtkinter import CTkLabel, CTkOptionMenu
from pasta.base.fstring_utils import placeholder
from tkinter import ttk
from customtkinter import CTkLabel, CTkOptionMenu
from pasta.base.fstring_utils import placeholder
from ttkwidgets.autocomplete import AutocompleteCombobox
import weightPerVolume as wv
import database as db
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

def tabWVSolutions(tabN, lbl):
    """ This function that creates an interface with necessary widgets for Weight to volume ratio widget."""

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

        selectedName = cboCompoundA.get()
        if selectedName:
            connection = connectDB()
            cursor = connection.cursor()
            chemicalFormula = fetchChemicalFormulas(cursor, selectedName)
            cboCompoundAF.set(chemicalFormula)
            cursor.close()
            connection.close()

    def clearFields():
        """Resets combobox and textboxes"""
        txtCompoundAWeight.delete(0, END)
        txtPercentage.delete(0, END)
        txtSolventAVolume.delete(0, END)

        cboCompoundA.set('')
        cboCompoundAF.set('')

    def calculateWV():
        """This function performs calculation for weight to volume operation on user input."""

        calculator = wv.WeightPerVolume()
        try:
            # Input the weight and volumes that will be used
            soluteWeight = txtCompoundAWeight.get().strip()
            soluteWeight = float(soluteWeight) if soluteWeight else None
            soluteUnit = cboCompoundAUnits.get().strip()

            solventVolume = txtSolventAVolume.get().strip()
            solventVolume = float(solventVolume) if solventVolume else None
            volumeUnit = cboSolventAVolumeUnits.get().strip()

            percentSolution = txtPercentage.get().strip()
            percentSolution = float(percentSolution) if percentSolution else None

            # Convert to grams and milliliters
            soluteWeight = calculator.convert_weight_to_grams(soluteWeight, soluteUnit) if soluteWeight and soluteUnit else None
            solventVolume = calculator.convert_volume_to_milliliters(solventVolume, volumeUnit) if solventVolume and volumeUnit else None

            # Calculate the missing value
            result = calculator.compute_solution(soluteWeight, solventVolume, percentSolution)

            if soluteWeight is None:
                result = f"The weight of solute needed is: {result:.2f} Grams."
            elif solventVolume is None:
                result = f"The volume of solvent needed is: {result:.2f} Milliliters."
            elif percentSolution is None:
                result = f"The percent solution is: {result:.2f}%."
            else:
                result = "Error: All inputs provided, but one should be left blank."
            lblOutput.configure(text=result)
        except ValueError as ve:
            lblOutput.configure(text=f"Error: Invalid input. Please enter numeric values. Details: {ve}")
        except Exception as e:
            lblOutput.configure(text=f"An error occurred: {e}")

        clearFields()

    lblTitle = customtkinter.CTkLabel(tabN, text=lbl, font=("Helvetica", 20), fg_color="#1a75ff", width=900, height=35,
                                      text_color="#404040")
    lblTitle.pack()


    lblCompoundA = customtkinter.CTkLabel(tabN, text="Compound A", width=200, font=("Helvetica", 15))
    lblCompoundA.pack()
    cboCompoundA = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundA.bind("<<ComboboxSelected>>", on_select)
    cboCompoundA.pack()

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

    # Calling function to populate combo box with chemical names
    populateChemicalNames()

    lblSolventAVolume = customtkinter.CTkLabel(tabN, text="Volume of Solvent A", font=("Helvetica", 15))
    lblSolventAVolume.pack()
    txtSolventAVolume = customtkinter.CTkEntry(tabN, width=300,border_color="#1a75ff")
    txtSolventAVolume.pack()

    lblSolventAVolumeUnits = customtkinter.CTkLabel(tabN, text="Units", font=("Helvetica", 15))
    lblSolventAVolumeUnits.pack()
    cboSolventAVolumeUnits = customtkinter.CTkOptionMenu(tabN, values=["Kiloliter", "Liter", "Milliliter"], width=300,
                                                    dropdown_font=("Helvetica", 19))

    cboSolventAVolumeUnits.pack()

    lblPercentage = customtkinter.CTkLabel(tabN, text="Percentage of Solution (%)", font=("Helvetica", 15))
    lblPercentage.pack()
    txtPercentage = customtkinter.CTkEntry(tabN, width=300,border_color="#1a75ff")
    txtPercentage.pack()

    # Button to perform Weight to Volume Ratio operation
    btnCalculate = customtkinter.CTkButton(tabN, text="Calculate",font=("Helvetica",15), width=300, command = calculateWV)
    btnCalculate.pack(pady=25)

    # Output Label
    lblOutput = customtkinter.CTkLabel(tabN, text="Output", font = ("Helvetica",15),fg_color="#1a75ff", width=800, height=35, text_color="#262626")
    lblOutput.pack()
