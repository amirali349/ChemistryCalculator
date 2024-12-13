# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides GUI based easy to use approach to perform various sophisticated chemical operations/calculations.
# This file creates interface for Stoichiometry operation on chemical compounds.

from tkinter import *
import customtkinter
from customtkinter import CTkLabel, CTkOptionMenu
from pasta.base.fstring_utils import placeholder
from tkinter import ttk
from customtkinter import CTkLabel, CTkOptionMenu
from pasta.base.fstring_utils import placeholder
from ttkwidgets.autocomplete import AutocompleteCombobox
import Stoichiometry as st
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
    """A function that fetch chemical Names of the compound from the compound database."""

    cursor.execute("SELECT ChemicalName FROM compounds")
    result = cursor.fetchall()
    names = [row['ChemicalName'] for row in result]
    return names


def fetchChemicalFormulas(cursor, cName):
    """A function that fetches chemical formula and Molecular weight of the compound based on the chemical name"""

    cursor.execute("SELECT ChemicalFormula FROM compounds where ChemicalName = %s",(cName,))
    result = cursor.fetchone()
    if result:
        return result['ChemicalFormula']
    return ""


def tabStoichiometry(tabN,lbl):
    """ This function that creates an interface with necessary widgets for Expected Yield Modules widget."""

    def calculateStoichiometry():
        """This function performs calculation for Stoichiometry operation on user input."""

        # Input variables
        compoundA = cboCompoundAF.get().strip()
        compoundB = cboCompoundBF.get().strip()
        productC = cboCompoundCF.get().strip()
        productD = cboCompoundDF.get().strip()

        balancer = st.ChemicalEquationBalancer(
            compoundA, compoundB, productC, productD,
        )

        coefficients = balancer.find_coefficients()

        coeffA, coeffB, coeffC, coeffD = coefficients.values()

        #print("\nBalanced equation coefficients:")

        result = f"Balanced equation coefficients: {coeffA}{compoundA} + {coeffB}{compoundB} = {coeffC}{productC} + {coeffD if coeffD else ''}{productD if productD else ''} "
        result2 = f" The Coefficients are: {coefficients}"

        lblOutput.configure(text=result)
        lblOutput2.configure(text=result2)

    def populateChemicalNames():
        """This function populates the comboboxes for compound A, B and Product C,D. with the chemical names of compound."""

        connection = connectDB()
        cursor = connection.cursor()
        chemical_names = fetchChemicalNames(cursor)
        cboCompoundA['completevalues'] = chemical_names
        cboCompoundB['completevalues'] = chemical_names
        cboProductC['completevalues'] = chemical_names
        cboProductD['completevalues'] = chemical_names
        cursor.close()
        connection.close()

    def on_selectA(event):
        """This function loads the chemical formula and molecular weight in their respective widgets based on chemical
        name selected for Product A."""
        selected_name = cboCompoundA.get()
        if selected_name:
            connection = connectDB()
            cursor = connection.cursor()
            chemical_formula = fetchChemicalFormulas(cursor, selected_name)
            cboCompoundAF.set(chemical_formula)
            cursor.close()
            connection.close()

    def on_selectB(event):
        """This function loads the chemical formula and molecular weight in their respective widgets based on chemical
        name selected for Product B."""

        selected_name = cboCompoundB.get()
        if selected_name:
            connection = connectDB()
            cursor = connection.cursor()
            chemical_formula = fetchChemicalFormulas(cursor, selected_name)
            cboCompoundBF.set(chemical_formula)
            cursor.close()
            connection.close()

    def on_selectC(event):
        """This function loads the chemical formula and molecular weight in their respective widgets based on chemical
        name selected for Product C."""

        selected_name = cboProductC.get()
        if selected_name:
            connection = connectDB()
            cursor = connection.cursor()
            chemical_formula = fetchChemicalFormulas(cursor, selected_name)
            cboCompoundCF.set(chemical_formula)
            cursor.close()
            connection.close()

    def on_selectD(event):
        """This function loads the chemical formula and molecular weight in their respective widgets based on chemical
        name selected for Product D."""

        selected_name = cboProductD.get()
        if selected_name:
            connection = connectDB()
            cursor = connection.cursor()
            chemical_formula = fetchChemicalFormulas(cursor, selected_name)
            cboCompoundDF.set(chemical_formula)
            cursor.close()
            connection.close()

    # Title
    lblTitle = customtkinter.CTkLabel(tabN, text=lbl, font=("Helvetica",20), fg_color="#1a75ff", width=900, height=35,text_color="#404040")
    lblTitle.pack(pady=10)

    # Product A
    lblCompoundA = customtkinter.CTkLabel(tabN, text="Compound A", width=200,font=("Helvetica",15))
    lblCompoundA.pack()

    cboCompoundA = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundA.bind("<<ComboboxSelected>>", on_selectA)
    #cboCompoundA = customtkinter.CTkOptionMenu(tabN, values=["Kilogram","Gram", "Milligram"], width=300, dropdown_font=("Helvetica",19))
    cboCompoundA.pack(pady = 5)

    lblCompoundAF = customtkinter.CTkLabel(tabN, text="Compound Formula", width=200, font=("Helvetica", 15))
    lblCompoundAF.pack()
    cboCompoundAF = AutocompleteCombobox(tabN, width=32, font=35)
    #cboCompoundAF.bind("<<ComboboxSelected>>", on_select)
    cboCompoundAF.pack()

    # Product B
    lblCompoundB = customtkinter.CTkLabel(tabN, text="Compound B", font=("Helvetica", 15))
    lblCompoundB.pack()
    cboCompoundB = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundB.bind("<<ComboboxSelected>>", on_selectB)
    cboCompoundB.pack(pady=5)
    lblCompoundBF = customtkinter.CTkLabel(tabN, text="Compound Formula", width=200, font=("Helvetica", 15))
    lblCompoundBF.pack()
    cboCompoundBF = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundBF.pack()

    # Product C
    lblProductC = customtkinter.CTkLabel(tabN, text="Product C",font=("Helvetica",15))
    lblProductC.pack()
    cboProductC = AutocompleteCombobox(tabN, width=32, font=35)
    cboProductC.bind("<<ComboboxSelected>>", on_selectC)
    cboProductC.pack(pady=5)
    lblCompoundCF = customtkinter.CTkLabel(tabN, text="Compound Formula", width=200, font=("Helvetica", 15))
    lblCompoundCF.pack()
    cboCompoundCF = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundCF.pack()

    # Product D
    lblProductD = customtkinter.CTkLabel(tabN, text="Product D", font=("Helvetica", 15))
    lblProductD.pack()
    cboProductD = AutocompleteCombobox(tabN, width=32, font=35)
    cboProductD.bind("<<ComboboxSelected>>", on_selectD)
    # cboCompoundA = customtkinter.CTkOptionMenu(tabN, values=["Kilogram","Gram", "Milligram"], width=300, dropdown_font=("Helvetica",19))
    cboProductD.pack(pady=5)
    lblCompoundDF = customtkinter.CTkLabel(tabN, text="Compound Formula", width=200, font=("Helvetica", 15))
    lblCompoundDF.pack()
    cboCompoundDF = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundDF.pack()

    # Calling function to populate combo boxes with chemical names
    populateChemicalNames()

    # Button to perform Expect Yield Module operation
    btnCalculate = customtkinter.CTkButton(tabN, text="Calculate",font=("Helvetica",15), width=300, command=calculateStoichiometry)
    btnCalculate.pack(pady = 30)

    # Output Labels
    lblOutput = customtkinter.CTkLabel(tabN, text="Output", font = ("Helvetica",16),fg_color="#1a75ff", width=800, height=30, text_color="#262626")
    lblOutput.pack(pady = 5)

    lblOutput2 = customtkinter.CTkLabel(tabN, text="Output", font = ("Helvetica",16),fg_color="#1a75ff", width=800, height=30, text_color="#262626")
    lblOutput2.pack(pady = 5)
