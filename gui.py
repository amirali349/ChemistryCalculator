# Author: Joseph Thomas, Amir Ali
# Date: December 9, 2024
# Project Title: Chemistry Calculator
# This project provides a GUI-based, easy-to-use approach to perform various sophisticated chemical operations/calculations.

from tkinter import *
import customtkinter
import tabDilution as td
import tabLimitingReactants as tl
import tabStoichiometry as ts
import tabExpectedYieldModules as te
import tabWWSolution as tw
import tabWVSolution as tv

class ChemistryCalculatorApp:
    """
    A class to represent the Chemistry Calculator application.
    """

    def __init__(self, root):
        """
        Constructor function that initializes all the necessary attributes for the Chemistry Calculator application.
        """
        self.root = root
        self.setupUI()

    def setupUI(self):
        """
        A function that sets up the user interface for the Chemistry Calculator application.
        """
        # Set appearance mode and theme
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")

        # Configure the main window
        self.root.title("Chemistry Calculator")
        self.root.geometry("700X700")
        self.root.minsize(900, 700)
        self.root.iconbitmap("icons1.ico")

        # Main label
        lblMain = customtkinter.CTkLabel(self.root, text="CHEMISTRY CALCULATOR", font=("Helvetica", 25), width=900,
                                         fg_color="#1a75ff", height=40, text_color="#404040")
        lblMain.pack()

        # Main tab view
        tabMain = customtkinter.CTkTabview(self.root, width=650, height=650, corner_radius=10)
        self.create_tabs(tabMain)
        tabMain.pack()

    def create_tabs(self, tabMain):
        """
         A function that creates and adds tabs to the main tab view.
        """
        # Create tabs for different chemical operations
        tabStoichiometry = tabMain.add("Stoichiometry Reactants")
        tabLimitingReactants = tabMain.add("Limiting Reactants")
        tabExpectedYieldModules = tabMain.add("Expected Yield Modules")
        # tabAcidBaseNeutralization = tabMain.add("Acid Base Neutralization")
        tabDilution = tabMain.add("Dilution")
        tabWWSolutions = tabMain.add("W-W-Solutions")
        tabWVSolutions = tabMain.add("W-V-Solutions")

        # Add content to each tab
        ts.tabStoichiometry(tabStoichiometry, "Stoichiometry Reactants")
        tl.tabLimitingReactants(tabLimitingReactants, "Limiting Reactants")
        te.tabExpectedYieldModules(tabExpectedYieldModules, "Expected Yield Modules")
        td.tabDilution(tabDilution, "Dilution")
        tw.tabWWSolutions(tabWWSolutions, "W/W Solution")
        tv.tabWVSolutions(tabWVSolutions, "W/V Solutions")


if __name__ == "__main__":
    # Main program execution
    root = customtkinter.CTk()
    app = ChemistryCalculatorApp(root)
    root.mainloop()
