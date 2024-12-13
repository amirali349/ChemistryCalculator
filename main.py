from weightPerWeight import WeightPerWeight
from weightPerVolume import WeightPerVolume
from dilution import DilutionCalculator
from Limiting_Reactant import LimitingReactant
from Stoichiometry import ChemicalEquationBalancer
from Expected_Yield import ExpectedYieldCalculator

# Test calculator function
def main():
    choice = 0

    # Loops through the calculator program until you hit -1 to quit.
    while choice != -1:
        calculator_choice = int(input("Which Calculator Would You Like to Use: "))

        # W-W-Calculator
        if calculator_choice == 1:
            calculator = WeightPerWeight()

            print("Weight per weight solution calculator")
            print("Enter the weight of Compound A (solute), Compound B (solvent), or the percent solution (leave one blank).")

            try:
                # input compound weights and units.
                compound_a = input("Weight of Compound A (solute, e.g., 10 g, 500 mg, or 0.01 kg): ").strip()
                compound_b = input("Weight of Compound B (solvent, e.g., 100 g, 1 kg, etc.): ").strip()
                # input percent solution
                percent_solution = input("Percent solution (w/w, e.g., 10): ").strip()

                # Parse inputs
                compound_a_weight, compound_a_unit = (float(compound_a.split()[0]), compound_a.split()[1]) if compound_a else (
                None, None)
                compound_b_weight, compound_b_unit = (float(compound_b.split()[0]), compound_b.split()[1]) if compound_b else (
                None, None)
                percent_solution = float(percent_solution) if percent_solution else None

                # Convert all weight to grams
                compound_a = calculator.convert_to_grams(compound_a_weight, compound_a_unit) if compound_a_weight else None
                compound_b = calculator.convert_to_grams(compound_b_weight, compound_b_unit) if compound_b_weight else None

                # Calculate the fourth value that was left blank
                result = calculator.compute_solution(compound_a, compound_b, percent_solution)

                if compound_a is None:
                    print(f"The weight of Compound A needed is: {result:.2f} grams.")
                elif compound_b is None:
                    print(f"The weight of Compound B needed is: {result:.2f} grams.")
                elif percent_solution is None:
                    print(f"The percent solution is: {result:.2f}%.")
                else:
                    print("Error: All inputs provided, but one should be left blank.")
            except Exception as e:
                print(f"An error occurred: {e}")

        # W-V-Calculator
        elif calculator_choice == 2:
            calculator = WeightPerVolume()

            print("Weight per volume solution calculator")
            print("Enter the weight of solute, volume of solvent, or the percent solution (leave one blank).")

            try:
                # input the weight and volumes that will be used.
                # solute is the same thing as compound A just the technical chemistry term for it
                solute_input = input("Weight of solute (e.g., 10 g, 500 mg, or 0.01 kg): ").strip()
                # solvent is the same as solvent A. Just a cleaner way to convey it to the user
                volume_input = input("Volume of solvent (e.g., 100 mL, 1 L, etc.): ").strip()
                percent_solution = input("Percent solution (w/v, e.g., 10): ").strip()

                # Parse inputs
                solute_weight, solute_unit = (
                float(solute_input.split()[0]), solute_input.split()[1]) if solute_input else (None, None)
                solvent_volume, volume_unit = (
                float(volume_input.split()[0]), volume_input.split()[1]) if volume_input else (None, None)
                percent_solution = float(percent_solution) if percent_solution else None

                # Convert to grams and milliliters
                solute_weight = calculator.convert_weight_to_grams(solute_weight, solute_unit) if solute_weight else None
                solvent_volume = calculator.convert_volume_to_milliliters(solvent_volume,
                                                                          volume_unit) if solvent_volume else None

                # Calculate the missing value
                result = calculator.compute_solution(solute_weight, solvent_volume, percent_solution)

                if solute_weight is None:
                    print(f"The weight of solute needed is: {result:.2f} grams.")
                elif solvent_volume is None:
                    print(f"The volume of solvent needed is: {result:.2f} milliliters.")
                elif percent_solution is None:
                    print(f"The percent solution is: {result:.2f}%.")
                else:
                    print("Error: All inputs provided, but one should be left blank.")
            except Exception as e:
                print(f"An error occurred: {e}")

        # Dilution Calculator
        elif calculator_choice == 3:
            calculator = DilutionCalculator()

            print("Dilution Calculator")
            print("Provide three of the following four values (leave one blank):")
            print("1. Concentration of Compound A (%), 2. Concentration of Compound B (%)")
            print("3. Volume of Compound A (e.g., 100 mL, 1 L, 0.01 kL)")
            print("4. Volume of Compound B (e.g., 500 mL, 2 L, 0.002 kL)")

            try:
                # input compound concentration and volume.
                conc_a = input("Concentration of Compound A (%): ").strip()
                conc_b = input("Concentration of Compound B (%): ").strip()
                vol_a = input("Volume of Compound A (e.g., 100 mL, 1 L, 0.01 kL): ").strip()
                vol_b = input("Volume of Compound B (e.g., 500 mL, 2 L, 0.002 kL): ").strip()

                # Parse inputs
                conc_a = float(conc_a) if conc_a else None
                conc_b = float(conc_b) if conc_b else None
                vol_a_value, vol_a_unit = (float(vol_a.split()[0]), vol_a.split()[1]) if vol_a else (None, None)
                vol_b_value, vol_b_unit = (float(vol_b.split()[0]), vol_b.split()[1]) if vol_b else (None, None)

                # Convert volumes to milliliters
                vol_a = calculator.convert_volume_to_milliliters(vol_a_value, vol_a_unit) if vol_a_value else None
                vol_b = calculator.convert_volume_to_milliliters(vol_b_value, vol_b_unit) if vol_b_value else None

                # Calculate the missing value
                result = calculator.compute_missing_value(conc_a, conc_b, vol_a, vol_b)

                if conc_a is None:
                    print(f"The concentration of Compound A is: {result:.2f}%.")
                elif conc_b is None:
                    print(f"The concentration of Compound B is: {result:.2f}%.")
                elif vol_a is None:
                    print(f"The volume of Compound A is: {result:.2f} mL.")
                elif vol_b is None:
                    print(f"The volume of Compound B is: {result:.2f} mL.")
                else:
                    print("Error: All inputs provided, but one should be left blank.")
            except Exception as e:
                print(f"An error occurred: {e}")

        # Stoichiometry Calculator
        elif calculator_choice == 4:
            # Just calls the main function in Stoichiometry.py which contains the prompts
            if __name__ == "__main__":
                balancer = ChemicalEquationBalancer()
                balancer.main()

        # Limiting Reactant Calculator
        elif calculator_choice == 5:
            print("Limiting Reactant Calculator")

            # Inputs for compound A. weight, units, and coefficient
            compound_a = input("Enter Compound A: ")
            weight_a = float(input(f"Enter the weight of {compound_a}: "))
            unit_a = input("Enter the unit of weight (mg, g, kg): ")
            coeff_a = int(input(f"Enter the molar coefficient of {compound_a}: "))

            # Inputs for compound B. weight, units, and coefficient
            compound_b = input("\nEnter Compound B: ")
            weight_b = float(input(f"Enter the weight of {compound_b}: "))
            unit_b = input("Enter the unit of weight (mg, g, kg): ")
            coeff_b = int(input(f"Enter the molar coefficient of {compound_b}: "))

            # Call LimitingReactant
            calculator = LimitingReactant(
                compound_a, weight_a, unit_a, coeff_a,
                compound_b, weight_b, unit_b, coeff_b
            )

            # Find the limiting reactant
            limiting = calculator.find_limiting_reactant()
            if limiting:
                print(f"\nThe limiting reactant is: {limiting}")
            else:
                print("\nReactants are in perfect stoichiometric ratio.")

        elif calculator_choice == 6:
            print("Expected Yield Calculator")

            # Inputs for compound A. weight, units, and coefficient
            compound_a = input("Enter Compound A: ")
            weight_a = float(input(f"Enter the weight of {compound_a}: "))
            unit_a = input("Enter the unit of weight (mg, g, kg): ")
            coeff_a = int(input(f"Enter the molar coefficient of {compound_a}: "))

            # Inputs for compound B. weight, units, and coefficient
            compound_b = input("Enter Compound B: ")
            weight_b = float(input(f"Enter the weight of {compound_b}: "))
            unit_b = input("Enter the unit of weight (mg, g, kg): ")
            coeff_b = int(input(f"Enter the molar coefficient of {compound_b}: "))

            product_c = input("Enter product C: ")
            coeff_c = int(input(f"Enter the molar coefficient of {product_c}: "))

            product_d = input("Enter product D: ")
            if product_d:
                try:
                    coeff_d = int(input(f"Enter the molar coefficient of {product_d}: "))
                except ValueError:
                    print("Invalid input for the coefficient. Setting it to None.")
                    coeff_d = None
            else:
                product_d = None
                coeff_d = None

            # Call Expected Yield
            calculator = ExpectedYieldCalculator(
                compound_a, weight_a, unit_a, coeff_a,
                compound_b, weight_b, unit_b, coeff_b,
                product_c, coeff_c,
                product_d, coeff_d
            )

            # Find the expected yield and store in variables for output for product_c and product_d
            expect_yield_product_c, expect_yield_product_d = calculator.find_expected_yield()
            print(f"The expected yield for {product_c} is: {expect_yield_product_c:.3f} grams")
            # Doesn't print anything if product_d doesn't exist
            if expect_yield_product_d is not None: print(f"The expected yield for {product_d} is: {expect_yield_product_d:.3f} grams")

        # Throws out error if 1 through 6 is not selected
        else:
            print("Error")
        # End the calculator program
        choice = int(input("Press -1 to end the program: "))



if __name__ == "__main__":
    main()