# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides GUI based easy to use approach to perform various sophisticated chemical operations/calculations.
# This file creates interface for Limiting Reactants calculation operation on chemical compounds.

import tkinter
from tkinter import *
import customtkinter
from tkinter import ttk
from customtkinter import CTkLabel, CTkOptionMenu
from pasta.base.fstring_utils import placeholder
from ttkwidgets.autocomplete import AutocompleteCombobox
import database as db
import Limiting_Reactant as lr
import pymysql
#from Stoichiometry import ChemicalEquationBalancer
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

def fetchChemicalDetails(cursor, cName):
    """A function that fetches chemical formula and Molecular weight of the compound based on the chemical name"""

    cursor.execute("SELECT ChemicalFormula, MolecularWeight FROM compounds where ChemicalName = %s", (cName,))
    result = cursor.fetchone()
    if result:
        return result['ChemicalFormula'], result['MolecularWeight']
    return "", None

def tabLimitingReactants(tabN,lbl):
    """ This function that creates an interface with necessary widgets for Limiting Reactant tab,"""

    lblTitle = customtkinter.CTkLabel(tabN, text=lbl, font=("Helvetica",20), fg_color="#1a75ff", width=900, height=35,text_color="#404040")
    lblTitle.pack(pady=10)

    def populateChemicalNames():
        """This function populates the comboboxes for compound A, B and Product C,D. with the chemical names of compound."""

        connection = connectDB()
        cursor = connection.cursor()
        chemical_names = fetchChemicalNames(cursor)
        cboCompoundA['completevalues'] = chemical_names
        cboCompoundB['completevalues'] = chemical_names
        cursor.close()
        connection.close()

    def on_selectA(event):
        """This function loads the chemical formula and molecular weight in their respective widgets based on chemical
         name selected for compound A."""

        selected_name = cboCompoundA.get()
        if selected_name:
            connection = connectDB()
            cursor = connection.cursor()
            chemical_formula, molecular_weight = fetchChemicalDetails(cursor, selected_name)
            cboCompoundAF.set(chemical_formula)
            txtCompoundAWeight.delete(0, END)
            #txtCompoundAWeight.insert(0, str(molecular_weight))
            cursor.close()
            connection.close()

    def on_selectB(event):
        """This function loads the chemical formula and molecular weight in their respective widgets based on chemical
         name selected for compound B."""

        selected_name = cboCompoundB.get()
        if selected_name:
            connection = connectDB()
            cursor = connection.cursor()
            chemical_formula, molecular_weight = fetchChemicalDetails(cursor, selected_name)
            cboCompoundBF.set(chemical_formula)
            txtCompoundBWeight.delete(0, END)
            #txtCompoundBWeight.insert(0, str(molecular_weight))
            cursor.close()
            connection.close()

    def calculateLimitingReactant():
        """This function performs calculation for Limiting Reactants on user input."""

        # Inputs for compound A. weight, units, and coefficient
        compound_a = cboCompoundAF.get().strip()
        weight_a = float(txtCompoundAWeight.get().strip())
        unit_a = cboCompoundAUnits.get().strip()
        coeff_a = float(txtCompoundACoefficient.get().strip())

        # Inputs for compound B. weight, units, and coefficient
        compound_b = cboCompoundBF.get().strip()
        weight_b = float(txtCompoundBWeight.get().strip())
        unit_b = cboCompoundBUnits.get().strip()
        coeff_b = float(txtCompoundBCoefficient.get().strip())

        #balancer = ChemicalEquationBalancer(
        #    compound_a, compound_b, product_c, product_d,
        #)

        #coefficients = balancer.find_coefficients()
        #coeff_a, coeff_b, coeff_c, coeff_d = coefficients.values()

        # Call LimitingReactant
        calculator = lr.LimitingReactant(
            compound_a, weight_a, unit_a, coeff_a,
            compound_b, weight_b, unit_b, coeff_b
        )

        # Find the limiting reactant
        limiting = calculator.find_limiting_reactant()
        if limiting:
            result = f"The limiting reactant is: {limiting}"
            lblOutput.configure(text=result)
        else:
            result = f"Reactants are in perfect stoichiometric ratio."
            lblOutput.configure(text=result)

        txtCompoundAWeight.delete(0,tkinter.END)
        txtCompoundBWeight.delete(0,tkinter.END)

    # Compound A
    lblCompoundA = customtkinter.CTkLabel(tabN, text="Compound A", width=200,font=("Helvetica",15))
    lblCompoundA.pack()
    cboCompoundA = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundA.bind("<<ComboboxSelected>>",on_selectA)
    cboCompoundA.pack()

    lblCompoundAF = customtkinter.CTkLabel(tabN, text="Compound Formula", width=200, font=("Helvetica", 15))
    lblCompoundAF.pack()
    cboCompoundAF = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundAF.pack()

    lblCompoundAWeight = customtkinter.CTkLabel(tabN, text="Compound A Weight",font=("Helvetica",15))
    lblCompoundAWeight.pack()
    txtCompoundAWeight = customtkinter.CTkEntry(tabN,width=300,border_color="#1a75ff")
    txtCompoundAWeight.pack()

    lblCompoundAUnits = customtkinter.CTkLabel(tabN, text="Units",width=300,font=("Helvetica",15))
    lblCompoundAUnits.pack()
    cboCompoundAUnits = customtkinter.CTkOptionMenu(tabN, values=["Kilogram", "Gram", "Milligram"],width=300,dropdown_font=("Helvetica",19))
    cboCompoundAUnits.pack()

    lblCompoundACoefficient = customtkinter.CTkLabel(tabN, text="Compound A Coefficient", font=("Helvetica", 15))
    lblCompoundACoefficient.pack()
    txtCompoundACoefficient = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtCompoundACoefficient.pack()

    # Compound B
    lblCompoundB = customtkinter.CTkLabel(tabN, text="Compound B",font=("Helvetica",15))
    lblCompoundB.pack()
    cboCompoundB = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundB.bind("<<ComboboxSelected>>", on_selectB)
    cboCompoundB.pack()

    lblCompoundBF = customtkinter.CTkLabel(tabN, text="Compound Formula", width=200, font=("Helvetica", 15))
    lblCompoundBF.pack()
    cboCompoundBF = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundBF.pack()

    lblCompoundBWeight = customtkinter.CTkLabel(tabN, text="Compound B Weight",font=("Helvetica",15))
    lblCompoundBWeight.pack()
    txtCompoundBWeight = customtkinter.CTkEntry(tabN,width=300,border_color="#1a75ff")
    txtCompoundBWeight.pack()

    lblCompoundBUnits = customtkinter.CTkLabel(tabN, text="Units",font=("Helvetica",15))
    lblCompoundBUnits.pack()
    cboCompoundBUnits = customtkinter.CTkOptionMenu(tabN, values=["Kilogram", "Gram", "Milligram"],width=300,dropdown_font=("Helvetica",19))
    cboCompoundBUnits.pack()

    lblCompoundBCoefficient = customtkinter.CTkLabel(tabN, text="Compound B Coefficient", font=("Helvetica", 15))
    lblCompoundBCoefficient.pack()
    txtCompoundBCoefficient = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtCompoundBCoefficient.pack()

    # Calling function to populate combo boxes with chemical names
    populateChemicalNames()

    # Button to perform Expect Yield Module operation
    btnCalculate = customtkinter.CTkButton(tabN, text="Output",font=("Helvetica",15), width=300, command=calculateLimitingReactant)
    btnCalculate.pack(pady = 5)

    # Output Label
    lblOutput = customtkinter.CTkLabel(tabN, text="Output", font = ("Helvetica",20),fg_color="#1a75ff", width=800, height=35, text_color="#262626")
    lblOutput.pack()
