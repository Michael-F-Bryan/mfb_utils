from utils import factorial


def test_factorial_positive_integer():
    fact = factorial(10)
    assert fact == 3628800
