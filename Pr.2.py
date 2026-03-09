def process_data(numbers):
    """
    Processes a list of numbers to find prime numbers and compute their factorial.

    This function iterates through the given list of integers, identifies the prime numbers,
    and calculates their factorial. The result is returned as a list of tuples,
    where each tuple contains a prime number and its respective factorial.

    :param numbers: The list of integers to be processed. Only positive integers greater
        than 1 will be considered for prime number and factorial calculation.
    :type numbers: list[int]

    :return: A list of tuples, each containing a prime number from the input
        list and its calculated factorial.
    :rtype: list[tuple[int, int]]
    """
    result = []
    for n in numbers:
        if n > 1:
            is_prime = True
            for i in range(2, n):
                if (n % i) == 0:
                    is_prime = False
                    break
            if is_prime:
                fact = 1
                for j in range(1, n + 1):
                    fact = fact * j
                result.append((n, fact))
    return result

data = [2, 3, 4, 5, 8, 10, 11]
print(process_data(data))