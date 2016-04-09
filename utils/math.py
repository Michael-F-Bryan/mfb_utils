"""
Miscellaneous math functions which aren't defined in the standard library math 
module.
"""


def factorial(number):
    """
    Find the factorial of a number through recursion.
    """
    if number != int(number):
        raise ValueError('number must be an integer.')

    if number > 1:
        total = 1
        for i in range(2, number + 1):
            total *= i
        return total
    elif number == 0 or number == 1:
        return 1
    else:
        raise ValueError('Factorial of a negative number is undefined.')
