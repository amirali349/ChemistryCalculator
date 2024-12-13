import pytest
from sympy import Eq
from Stoichiometry import ChemicalEquationBalancer


@pytest.fixture
def balancer():
    return ChemicalEquationBalancer()


def test_parse_formula(balancer):
    # Test for a single compound
    formula = "CH4"
    expected = {"C": 1, "H": 4}
    assert balancer.parse_formula(formula) == expected

    # Test for nested parentheses and multipliers
    formula = "Ca(OH)2"
    expected = {"Ca": 1, "O": 2, "H": 2}
    assert balancer.parse_formula(formula) == expected

    # Test for compounds with complex parentheses
    formula = "Al2(SO4)3"
    expected = {"Al": 2, "S": 3, "O": 12}
    assert balancer.parse_formula(formula) == expected


def test_combine_counts(balancer):
    # Test combining multiple dictionaries
    dict1 = {"C": 1, "H": 4}
    dict2 = {"O": 2, "H": 2}
    expected = {"C": 1, "H": 6, "O": 2}
    assert balancer.combine_counts(dict1, dict2) == expected


def test_solve_linear_system(balancer):
    # Test solving a linear system of equations
    equations = [
        Eq(balancer.a, balancer.c),
        Eq(4* balancer.a, 2 * balancer.d),
        Eq(2*balancer.b, 2 * balancer.c + balancer.d),
    ]
    a_guess = 1
    solution = balancer.solve_linear_system(equations, a_guess)
    expected = {balancer.a: 1, balancer.b: 2, balancer.c: 1, balancer.d: 2}
    assert solution == expected


def test_balance_equation(balancer):
    # Test balancing a simple chemical equation
    counts_a = {"C": 1, "H": 4}
    counts_b = {"O": 2}
    counts_c = {"C": 1, "O": 2}
    counts_d = {"H": 2, "O": 1}
    coefficients = balancer.balance_equation(counts_a, counts_b, counts_c, counts_d)
    expected = {balancer.a: 1, balancer.b: 2, balancer.c: 1, balancer.d: 2}
    assert coefficients == expected

