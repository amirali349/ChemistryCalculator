import pytest
from Limiting_Reactant import LimitingReactant

def test_get_molar_mass():
    calculator = LimitingReactant("CH4", 0, "g", 1, "O2", 0, "g", 1)
    assert calculator.get_molar_mass("CH4") == 16.04
    assert calculator.get_molar_mass("O2") == 32.00
    assert calculator.get_molar_mass("Invalid") is None

def test_convert_to_grams():
    calculator = LimitingReactant("CH4", 0, "g", 1, "O2", 0, "g", 1)
    assert calculator.convert_to_grams(1000, "mg") == 1
    assert calculator.convert_to_grams(1, "g") == 1
    assert calculator.convert_to_grams(1, "kg") == 1000

def test_calculate_moles():
    calculator = LimitingReactant("CH4", 0, "g", 1, "O2", 0, "g", 1)
    assert calculator.calculate_moles(10, 16.04) == pytest.approx(0.623, rel=1e-3)
    assert calculator.calculate_moles(200, 32.00) == 6.25

def test_invalid_unit():
    lr = LimitingReactant(
        compound_a="CH4", weight_a=32, unit_a="lb", coeff_a=1,
        compound_b="O2", weight_b=96, unit_b="g", coeff_b=2
    )
    with pytest.raises(KeyError):
        lr.convert_to_grams(lr.weight_a, lr.unit_a)

