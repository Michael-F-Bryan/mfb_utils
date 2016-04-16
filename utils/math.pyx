cpdef double average(list data):
    cdef:
        double total = 0, i

    for i in data:
        total += i

    return total/len(data)


cdef _sieve_of_erosthenes(int n):
    """
    A naive implementation of the sieve of erosthenes that returns a list of
    all primes below `n`. 

    Note that all type and value checking is done by a python wrapper.
    """

    cdef:
        list primes = []
        int i, number
        list sieve = [True for i in range(n + 1)]

    for number in range(2, n + 1):
        if sieve[number]:
           primes.append(number)
           for i in range(number * number, n + 1, number):
               sieve[i] = False
    return primes


def sieve_of_erosthenes(n):
    """
    A thin python wrapper function around _sieve_of_erosthenes() to do all 
    type and value checking.
    """
    if not isinstance(n, int):
        raise TypeError('n must be a positive integer')
    if n <= 0 or int(n) != n:
        raise ValueError('n must be a positive integer')

    return _sieve_of_erosthenes(n)

