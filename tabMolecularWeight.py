import customtkinter
from ttkwidgets.autocomplete import AutocompleteCombobox
import Stoichiometry as st
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


def tabMolecularWeight(tabN,lbl):
    """ This function that creates an interface with necessary widgets for Expected Yield Modules widget."""

    def calculateStoichiometry():
        """This function performs calculation for Stoichiometry operation on user input."""

        # Input variables
        compoundA = cboCompoundAF.get().strip()
        compoundB = 0
        productC = 0
        productD = 0

        balancer = st.ChemicalEquationBalancer(
            compoundA, compoundB, productC, productD,
        )

        molar_mass_a, molar_mass_b, molar_mass_c, molar_mass_d = balancer.find_molecular_weight()

        result = f"Molecular Weight of {compoundA} is {molar_mass_a:.3f} g/mol"
        #result2 = f" The Coefficients are: {coefficients}"

        lblOutput.configure(text=result)

    def populateChemicalNames():
        """This function populates the comboboxes for compound A, B and Product C,D. with the chemical names of compound."""

        connection = connectDB()
        cursor = connection.cursor()
        chemical_names = fetchChemicalNames(cursor)
        cboCompoundA['completevalues'] = chemical_names
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


    # Calling function to populate combo boxes with chemical names
    populateChemicalNames()

    # Button to perform Expect Yield Module operation
    btnCalculate = customtkinter.CTkButton(tabN, text="Calculate",font=("Helvetica",15), width=300, command=calculateStoichiometry)
    btnCalculate.pack(pady = 30)

    # Output Labels
    lblOutput = customtkinter.CTkLabel(tabN, text="Output", font = ("Helvetica",16),fg_color="#1a75ff", width=800, height=30, text_color="#262626")
    lblOutput.pack(pady = 5)
