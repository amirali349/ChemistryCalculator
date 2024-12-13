# ChemistryCalculator
This is a python application that provides GUI interface to perform various chemical operations easily.
Please install the following libraries and software:
1. CustomTkinter
2. Pymysql
3. Sympy
4. ttkwidgets
5  openpyxl
6. MySQL Database Management System (latest version)
Database Login Details
User: Root
Password: Chemistry.123

Instructions to run the calculator:
1. Download all the files and load into your IDE.
2. Ensure all python libraries have successfully installed.
3. Run the database.py file to create the MYSQL database.
4. Run the gui.py file and wait for the interface to load.
5. To enter a compound, type the first few letters then select the pulldown menu and click on the full name.
6. E.g for "Hydrogen" type "Hyd" click the dropdown and pick "Hydrogen" then H2 will fill in the blank.
7. If the full chemical name is typed and not selected then the chemical formula will not fill in where it's supposed to

Individual Tabs: Test Chemical Equation: N2 + H2 = NH3
1. For Stoichiometry enter a valid Chemical Equation. E.g Compound A = N2; Compound B = H2; Product C = NH3; Product left blank
2. The Equation will balance itself and display at the bottom.
3. For Limiting Reactant enter the same Chemical Equation "Compounds" but this time input their weights as well.
4. No need to balance the equation. All that will be done when you select output and the limiting reactant will be shown
5. For Expected Yield enter the same as Limiting Reactant but this time include the "Products"
6. The expected yield for the chemical reaction for both products will be displayed. Product D won't display if it is 0.
7. For Dilution enter 3 out of the 4 quantities listed in the menu. The 4th will be calculated automatically.
8. For W-W Solutions enter the name of the compound and then 2 out of the 3 quantities listed (Mass of compound A, Mass of solvent A, Percentage). The 3rd will be calculated automatically.
9. For W-V Solutions enter the name of the compound and then 2 out of the 3 quantities listed (Mass of compound A, Volume of solvent A, Percentage). The 3rd will be calculated automatically.

****************************************************************************************************************************************
***Side Note the database is limited to only 65 compounds currently (ran out of time to automate and validate). 
***This limits the total combination of Valid Chemical Equations. Some examples are:
***Salt double replacements using Cl, Br, or NO3. LiOH + NaCl = LiCl + NaOH
***Burning reactions that produce CO2 and H2O. C6H12O6 (glucose) + O2 = CO2 + H2O
***Gases: S + O2 = SO2; H2 + O2 = H2O; N2 + O2 = NO2;
***If your database is missing Water or Carbon dioxide please delete the old SQL database and use the database.csv file from this Repo
****************************************************************************************************************************************

*********************************************************************************
Please use gui.py as main file for start of the Chemistry Calculator Application
*********************************************************************************
