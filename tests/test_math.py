from utils.math import factorial
import pytest


def test_factorial_negative_integer():
    with pytest.raises(ValueError):
        fact = factorial(-10)


def test_factorial_positive_integer():
    fact = factorial(10)
    assert fact == 3628800


def test_factorial_zero():
    fact = factorial(0)
    assert fact == 1


def test_factorial_one():
    fact = factorial(1)
    assert fact == 1


def test_factorial_noninteger():
    with pytest.raises(ValueError):
        fact = factorial(12.3)


def test_factorial_string():
    with pytest.raises(ValueError):
        fact = factorial('stuff')

