from Limiting_Reactant import LimitingReactant
from Stoichiometry import ChemicalEquationBalancer
from Expected_Yield import ExpectedYieldCalculator
from dilution import DilutionCalculator
from weightPerWeight import WeightPerWeight
from weightPerVolume import WeightPerVolume


def main():
    while True:
        print("Options:")
        print("1. Stoichiometry Calculator")
        print("2. Limiting Reactant Calculator")
        print("3. Expected Yield Calculator")
        print("4. Dilution Calculator")
        print("5. w/w Solution Calculator")
        print("6. w/v Solution Calculator")
        print("-1. Quit")

        choice = int(input("Select an option: "))
        if choice == -1:
            print("Exiting program.")
            break
        elif choice == 1:

            print("Enter the chemical compounds in the equation:")
            # Input variables
            compound_a = input("Compound A (e.g., CH4): ")
            compound_b = input("Compound B (e.g., O2): ")
            product_c = input("Product C (e.g., CO2): ")
            product_d = input("Product D (e.g., H2O): ")

            balancer = ChemicalEquationBalancer(
                compound_a, compound_b, product_c, product_d,
            )

            coefficients = balancer.find_coefficients()

            molar_mass_a, molar_mass_b, molar_mass_c, molar_mass_d = balancer.find_molecular_weight()
            #print(molar_mass_a, molar_mass_b, molar_mass_c, molar_mass_d)

            coeff_a, coeff_b, coeff_c, coeff_d = coefficients.values()

            print("\nBalanced equation coefficients:")
            # Final line ensures nothing is printed if product D is left blank
            print(f"{coeff_a}{compound_a} + {coeff_b}{compound_b} = {coeff_c}{product_c} + {coeff_d if coeff_d else ''}{product_d if product_d else ''}")

            print(coefficients)
        elif choice == 2:

            print("Enter the chemical compounds in the equation:")
            # Input variables
            compound_a = input("Compound A (e.g., CH4): ")
            compound_b = input("Compound B (e.g., O2): ")
            product_c = input("Product C (e.g., CO2): ")
            product_d = input("Product D (e.g., H2O): ")

            balancer = ChemicalEquationBalancer(
                compound_a, compound_b, product_c, product_d,
            )

            coefficients = balancer.find_coefficients()
            coeff_a, coeff_b, coeff_c, coeff_d = coefficients.values()

            weight_a = float(input(f"Enter the weight of {compound_a}: "))
            unit_a = input("Enter the unit of weight (mg, g, kg): ")

            weight_b = float(input(f"Enter the weight of {compound_b}: "))
            unit_b = input("Enter the unit of weight (mg, g, kg): ")

            calculator = LimitingReactant(
                compound_a, weight_a, unit_a, coeff_a,
                compound_b, weight_b, unit_b, coeff_b
            )
            limiting = calculator.find_limiting_reactant()
            if limiting:
                print(f"The limiting reactant is: {limiting}")
            else:
                print("Reactants are in perfect stoichiometric ratio.")

        elif choice == 3:
            print("Enter the chemical compounds in the equation:")
            # Input variables
            compound_a = input("Compound A (e.g., CH4): ")
            compound_b = input("Compound B (e.g., O2): ")
            product_c = input("Product C (e.g., CO2): ")
            product_d = input("Product D (e.g., H2O): ")

            balancer = ChemicalEquationBalancer(
                compound_a, compound_b, product_c, product_d,
            )

            coefficients = balancer.find_coefficients()
            coeff_a, coeff_b, coeff_c, coeff_d = coefficients.values()

            weight_a = float(input(f"Enter the weight of {compound_a}: "))
            unit_a = input("Enter the unit of weight (mg, g, kg): ")

            weight_b = float(input(f"Enter the weight of {compound_b}: "))
            unit_b = input("Enter the unit of weight (mg, g, kg): ")

            calculator = ExpectedYieldCalculator(
                compound_a, weight_a, unit_a, coeff_a,
                compound_b, weight_b, unit_b, coeff_b,
                product_c, coeff_c,
                product_d, coeff_d
            )

            expect_yield_product_c, expect_yield_product_d = calculator.find_expected_yield()
            print(f"The expected yield for {product_c} is: {expect_yield_product_c:.3f} grams")
            # Doesn't print anything if product_d doesn't exist
            if expect_yield_product_d is not None and expect_yield_product_d != 0: print(f"The expected yield for {product_d} is: {expect_yield_product_d:.3f} grams")

        elif choice == 4:

            print("Dilution Calculator")

            try:
                # input compound concentration and volume.
                conc_a = float(input("Concentration of Compound A (%): "))
                conc_b = float(input("Concentration of Compound B (%): "))
                vol_a = input("Volume of Compound A (e.g., 100 ): ")
                vol_a = float(vol_a) if vol_a.strip() else None
                unit_a = input("Enter the unit of volume (mL, L, kL): ")
                vol_b = (input("Volume of Compound B (e.g., 500 ): "))
                vol_b = float(vol_b) if vol_b.strip() else None
                unit_b = input("Enter the unit of volume (mL, L, kL): ")

                calculator = DilutionCalculator(conc_a, conc_b, vol_a, vol_b, unit_a, unit_b)

                # Calculate the missing value
                result = calculator.compute_missing_value()

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

        elif choice == 5:

            print("Weight per weight solution calculator")
            try:
                # input compound weights and units.
                compound_a = input("Weight of Compound A (solute, e.g., 10 ): ")
                compound_a = float(compound_a) if compound_a.strip() else None
                unit_a = input("Enter the unit of weight (mg, g, kg): ")
                compound_b = input("Weight of Compound B (solvent, e.g., 100 ): ")
                compound_b = float(compound_b) if compound_b.strip() else None
                unit_b = input("Enter the unit of weight (mg, g, kg): ")

                # input percent solution
                percent_solution = input("Percent solution (w/w, e.g., 10): ")
                percent_solution = float(percent_solution) if percent_solution.strip() else None

                calculator = WeightPerWeight(compound_a, compound_b, percent_solution, unit_a, unit_b)

                # Calculate the fourth value that was left blank
                result = calculator.compute_solution()

                if compound_a is None:
                    print(f"The weight of Compound A needed is: {result:.3f} grams.")
                elif compound_b is None:
                    print(f"The weight of Compound B needed is: {result:.3f} grams.")
                elif percent_solution is None:
                    print(f"The percent solution is: {result:.3f}%.")
                else:
                    print("Error: All inputs provided, but one should be left blank.")
            except Exception as e:
                print(f"An error occurred: {e}")

        elif choice == 6:

            print("Weight per volume solution calculator")

            try:
                # input the weight and volumes that will be used.
                compound_a = input("Weight of solute (e.g., 10): ")
                compound_a = float(compound_a) if compound_a.strip() else None
                unit_a = input("Enter the unit of weight (mg, g, kg): ")
                solvent_a = input("Volume of solvent (e.g., 100 ): ")
                solvent_a = float(solvent_a) if solvent_a.strip() else None
                unit_b = input("Enter the unit of volume (mL, L, kL): ")
                percent_solution = input("Percent solution (w/v, e.g., 10): ")
                percent_solution = float(percent_solution) if percent_solution.strip() else None

                calculator = WeightPerVolume(compound_a, solvent_a, percent_solution, unit_a, unit_b)

                # Calculate the missing value
                result = calculator.compute_solution()

                if compound_a is None:
                    print(f"The weight of solute needed is: {result:.3f} grams.")
                elif solvent_a is None:
                    print(f"The volume of solvent needed is: {result:.3f} milliliters.")
                elif percent_solution is None:
                    print(f"The percent solution is: {result:.3f}%.")
                else:
                    print("Error: All inputs provided, but one should be left blank.")
            except Exception as e:
                print(f"An error occurred: {e}")

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()