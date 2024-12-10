# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides GUI based easy to use approach to perform various sophisticated chemical operations/calculations.
# This file creates interface for Expected Yield Module operation on chemical compounds.

from tkinter import *
import customtkinter
from customtkinter import CTkLabel, CTkOptionMenu, CTkEntry
from pasta.base.fstring_utils import placeholder
from tkinter import ttk
from customtkinter import CTkLabel, CTkOptionMenu
from pasta.base.fstring_utils import placeholder
from ttkwidgets.autocomplete import AutocompleteCombobox
import Expected_Yield as ey
import database as db
import pymysql
import database as db

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

def tabExpectedYieldModules(tabN, lbl):
    """ This function that creates an interface with necessary widgets for Expected Yield Modules widget."""

    def clearFields():
        """Resets combobox and textboxes"""
        txtCompoundAWeight.delete(0, END)
        txtCompoundBWeight.delete(0, END)
        txtCompoundCWeight.delete(0, END)
        txtCompoundDWeight.delete(0, END)
        txtCompoundACoefficient.delete(0, END)
        txtCompoundBCoefficient.delete(0, END)
        txtProductCCoefficient.delete(0, END)
        txtProductDCoefficient.delete(0, END)

        cboCompoundA.set('')
        cboCompoundB.set('')
        cboProductC.set('')
        cboProductD.set('')
        cboCompoundAF.set('')
        cboCompoundBF.set('')
        cboCompoundCF.set('')
        cboCompoundDF.set('')

    def CalculateExpectedYieldModules():
        """This function performs calculation for expected yield module operation on user input."""

        # Inputs for compound A. weight, units, and coefficient
        compoundA = cboCompoundAF.get().strip()
        weightA = float(txtCompoundAWeight.get().strip())
        unitA = cboCompoundAUnits.get().strip()
        coeffA = float(txtCompoundACoefficient.get().strip())

        # Inputs for compound B. weight, units, and coefficient
        compoundB = cboCompoundBF.get().strip()
        weightB = float(txtCompoundBWeight.get().strip())
        unitB = cboCompoundBUnits.get().strip()
        coeffB = float(txtCompoundBCoefficient.get().strip())

        productC = cboCompoundCF.get().strip()
        weightC = float(txtCompoundCWeight.get().strip())
        coeffC = float(txtProductCCoefficient.get().strip())

        weightD = float(txtCompoundDWeight.get().strip())

        productD = cboCompoundDF.get().strip()
        if productD:
            try:
                coeffD = float(txtProductDCoefficient.get().strip())
            except ValueError:
                result = "Invalid input for the coefficient. Setting it to None."
                lblOutput.configure(text=result)
                coeffD = None
        else:
            productD = None
            coeffD = None

        # Call Expected Yield
        calculator = ey.ExpectedYieldCalculator(
            compoundA, weightA, unitA, coeffA,
            compoundB, weightB, unitB, coeffB,
            productC, coeffC,
            productD, coeffD
        )

        # Find the expected yield and store in variables for output for product_c and product_d
        expect_yield_product_c, expect_yield_product_d = calculator.find_expected_yield(weightA,weightB,weightC,weightD)
        result = f"The expected yield for {productC} is: {expect_yield_product_c:.3f} grams"
        lblOutput.configure(text=result)
        # Doesn't print anything if product_d doesn't exist
        if expect_yield_product_d is not None:
            result = f"The expected yield for {productD} is: {expect_yield_product_d:.3f} grams"
            lblOutput.configure(text=result)

        clearFields()


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
        name selected for compound A."""
        selected_name = cboCompoundA.get()
        if selected_name:
            connection = connectDB()
            cursor = connection.cursor()
            chemical_formula, molecular_weight = fetchChemicalDetails(cursor, selected_name)
            cboCompoundAF.set(chemical_formula)
            txtCompoundAWeight.delete(0, END)
            txtCompoundAWeight.insert(0, str(molecular_weight))
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
            txtCompoundBWeight.insert(0, str(molecular_weight))
            cursor.close()
            connection.close()

    def on_selectC(event):
        """This function loads the chemical formula and molecular weight in their respective widgets based on chemical
        name selected for Product C."""
        selected_name = cboProductC.get()
        if selected_name:
            connection = connectDB()
            cursor = connection.cursor()
            chemical_formula, molecular_weight = fetchChemicalDetails(cursor, selected_name)
            cboCompoundCF.set(chemical_formula)
            txtCompoundCWeight.delete(0, END)
            txtCompoundCWeight.insert(0, str(molecular_weight))
            cursor.close()
            connection.close()

    def on_selectD(event):
        """This function loads the chemical formula and molecular weight in their respective widgets based on chemical
        name selected for Product D."""
        selected_name = cboProductD.get()
        if selected_name:
            connection = connectDB()
            cursor = connection.cursor()
            chemical_formula, molecular_weight = fetchChemicalDetails(cursor, selected_name)
            cboCompoundDF.set(chemical_formula)
            txtCompoundDWeight.delete(0, END)
            txtCompoundDWeight.insert(0, str(molecular_weight))
            cursor.close()
            connection.close()
    #Title
    lblTitle = customtkinter.CTkLabel(tabN, text=lbl, font=("Helvetica", 20), fg_color="#1a75ff", height=35, width=900, text_color="#404040")
    lblTitle.grid(row=0, column=0, columnspan=900, pady=5)
    # Compound A widgets
    lblCompoundA = customtkinter.CTkLabel(tabN, text="Compound A", width=200, font=("Helvetica", 15))
    lblCompoundA.grid(row=1, column=0, pady=1)

    cboCompoundA = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundA.grid(row=1, column=1, pady=1)
    cboCompoundA.bind("<<ComboboxSelected>>", on_selectA)

    lblCompoundAF = customtkinter.CTkLabel(tabN, text="Compound Formula", width=200, font=("Helvetica", 15))
    lblCompoundAF.grid(row=2, column=0, pady=1)

    cboCompoundAF = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundAF.grid(row=2, column=1, pady=1)

    lblCompoundAWeight = customtkinter.CTkLabel(tabN, text="Compound A Weight", font=("Helvetica", 15))
    lblCompoundAWeight.grid(row=3, column=0, pady=1)

    txtCompoundAWeight = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtCompoundAWeight.grid(row=3, column=1, pady=1)

    lblCompoundAUnits = customtkinter.CTkLabel(tabN, text="Units", width=300, font=("Helvetica", 15))
    lblCompoundAUnits.grid(row=4, column=0, pady=1)

    cboCompoundAUnits = customtkinter.CTkOptionMenu(tabN, values=["Kilogram", "Gram", "Milligram"], width=300, dropdown_font=("Helvetica", 19))
    cboCompoundAUnits.grid(row=4, column=1, pady=1)

    lblCompoundACoefficient = customtkinter.CTkLabel(tabN, text="Compound A Coefficient", font=("Helvetica", 15))
    lblCompoundACoefficient.grid(row=5, column=0, pady=1)

    txtCompoundACoefficient = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtCompoundACoefficient.grid(row=5, column=1, pady=1)
    # Compound B widgets
    lblCompoundB = customtkinter.CTkLabel(tabN, text="Compound B", font=("Helvetica", 15))
    lblCompoundB.grid(row=6, column=0, pady=1)

    cboCompoundB = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundB.grid(row=6, column=1, pady=1)
    cboCompoundB.bind("<<ComboboxSelected>>", on_selectB)

    lblCompoundBF = customtkinter.CTkLabel(tabN, text="Compound Formula", width=200, font=("Helvetica", 15))
    lblCompoundBF.grid(row=7, column=0, pady=1)

    cboCompoundBF = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundBF.grid(row=7, column=1, pady=1)

    lblCompoundBWeight = customtkinter.CTkLabel(tabN, text="Compound B Weight", font=("Helvetica", 15))
    lblCompoundBWeight.grid(row=8, column=0, pady=1)

    txtCompoundBWeight = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtCompoundBWeight.grid(row=8, column=1, pady=1)

    lblCompoundBUnits = customtkinter.CTkLabel(tabN, text="Units", font=("Helvetica", 15))
    lblCompoundBUnits.grid(row=9, column=0, pady=1)

    cboCompoundBUnits = customtkinter.CTkOptionMenu(tabN, values=["Kilogram", "Gram", "Milligram"], width=300, dropdown_font=("Helvetica", 19))
    cboCompoundBUnits.grid(row=9, column=1, pady=1)

    lblCompoundBCoefficient = customtkinter.CTkLabel(tabN, text="Compound B Coefficient", font=("Helvetica", 15))
    lblCompoundBCoefficient.grid(row=10, column=0, pady=1)

    txtCompoundBCoefficient = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtCompoundBCoefficient.grid(row=10, column=1, pady=1)

    # Product C widgets
    lblProductC = customtkinter.CTkLabel(tabN, text="Product C", font=("Helvetica", 15))
    lblProductC.grid(row=11, column=0, pady=1)

    cboProductC = AutocompleteCombobox(tabN, width=32, font=35)
    cboProductC.grid(row=11, column=1, pady=1)
    cboProductC.bind("<<ComboboxSelected>>", on_selectC)

    lblCompoundCF = customtkinter.CTkLabel(tabN, text="Compound Formula", width=200, font=("Helvetica", 15))
    lblCompoundCF.grid(row=12, column=0, pady=1)

    cboCompoundCF = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundCF.grid(row=12, column=1, pady=1)

    lblCompoundCWeight = customtkinter.CTkLabel(tabN, text="Compound C Weight", font=("Helvetica", 15))
    lblCompoundCWeight.grid(row=13, column=0, pady=1)

    txtCompoundCWeight = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtCompoundCWeight.grid(row=13, column=1, pady=1)

    lblProductCCoefficient = customtkinter.CTkLabel(tabN, text="Product C Coefficient", font=("Helvetica", 15))
    lblProductCCoefficient.grid(row=14, column=0, pady=3)

    txtProductCCoefficient = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtProductCCoefficient.grid(row=14, column=1, pady=1)

    # Product C widgets
    lblProductD = customtkinter.CTkLabel(tabN, text="Product D", font=("Helvetica", 15))
    lblProductD.grid(row=15, column=0, pady=1)

    cboProductD = AutocompleteCombobox(tabN, width=32, font=35)
    cboProductD.grid(row=15, column=1, pady=1)
    cboProductD.bind("<<ComboboxSelected>>", on_selectD)

    lblCompoundDF = customtkinter.CTkLabel(tabN, text="Compound Formula", width=200, font=("Helvetica", 15))
    lblCompoundDF.grid(row=16, column=0, pady=1)

    cboCompoundDF = AutocompleteCombobox(tabN, width=32, font=35)
    cboCompoundDF.grid(row=16, column=1, pady=1)

    lblCompoundDWeight = customtkinter.CTkLabel(tabN, text="Compound A Weight", font=("Helvetica", 15))
    lblCompoundDWeight.grid(row=17, column=0, pady=1)

    txtCompoundDWeight = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtCompoundDWeight.grid(row=17, column=1, pady=1)

    lblProductDCoefficient = customtkinter.CTkLabel(tabN, text="Product D Coefficient", font=("Helvetica", 15))
    lblProductDCoefficient.grid(row=18, column=0, pady=1)

    txtProductDCoefficient = customtkinter.CTkEntry(tabN, width=300, border_color="#1a75ff")
    txtProductDCoefficient.grid(row=18, column=1, pady=1)

    # Calling function to populate combo boxes with chemical names
    populateChemicalNames()

    # Button to perform Expect Yield Module operation
    btnCalculate = customtkinter.CTkButton(tabN, text="Calculate", font=("Helvetica", 15), width=300, command=CalculateExpectedYieldModules)
    btnCalculate.grid(row=19, column=1, pady=10)

    # Output Label
    lblOutput = customtkinter.CTkLabel(tabN, text="Output", font=("Helvetica", 20), fg_color="#1a75ff", width=800, height=40, text_color="#262626")
    lblOutput.grid(row=20, column=0, columnspan=900, pady=5)
