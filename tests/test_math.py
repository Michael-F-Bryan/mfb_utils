"""
The test suite for the math module of my utils package.
"""

from utils import math
import pytest
import random


def test_average_valid_input_random():
    random.seed(5)

    numbers = [random.random()*10 for i in range(10)]
    should_be = sum(numbers)/len(numbers)
    print(numbers)

    assert should_be == math.average(numbers)

def test_average_valid_input():
    numbers = [1, 2, 3, 4, 5, 6, 7]
    should_be = sum(numbers)/len(numbers)

    assert should_be == math.average(numbers)


def test_average_invalid_input():
    numbers = "some random string"
    
    with pytest.raises(TypeError):
        math.average(numbers)


def test_sieve_valid_input():
    primes = math.sieve_of_erosthenes(5)
    assert primes == [2, 3, 5]


def test_sieve_negative_number():
    with pytest.raises(ValueError):
        math.sieve_of_erosthenes(-3)


def test_sieve_decimal_input():
    with pytest.raises(TypeError):
        math.sieve_of_erosthenes(5.5)


def test_sieve_string_input():
    with pytest.raises(TypeError):
        math.sieve_of_erosthenes('hello')

