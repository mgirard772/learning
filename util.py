import string
import itertools
import random


def int_to_ssn(x: int = 0, dashes=True):
    """Converts an int into SSN format

    Args:
        x (int): Integer to convert to an SSN. Should be between 0 and 999,999,999 inclusive.
        dashes (bool): Boolean indicating if dashes should be included in string

    Returns:
        str: String converted into an SSN.

    Raises:
        ValueError: Raises a ValueError if x is not an integer, None, negative, or greater than 999,999,999
    """
    if type(x) is not int:
        raise ValueError(
            f"x ({x}) is not an integer"
        )
    if x < 0 or x > (10**9)-1:
        raise ValueError(
            f"x ({x}) is not a valid SSN integer. Must be between 0 and %d inclusive." % (10**9-1)
        )
    x = str(x)
    x = "0"*(9-x.__len__())+x
    if dashes:
        x = "%s-%s-%s" % (x[0:3], x[3:5], x[5:9])
    return x


def random_ssn(number: int = 1, dashes: bool = True, unique: bool = False):
    """
    Return a random SSN or list of SSN's

    Args:
        number (int): Number of SSN's to return. If blank, None or 1, a single string will be returned. (default is 1)
        dashes (bool): Boolean indicated if dashes should be included in SSN string. (default is True)
        unique (bool): Boolean indicating if returned SSN's should be unique. (default is False)

    Returns:
        List[str]: An SSN string or list of SSN strings

    Raises:
        ValueError: Raises a ValueError if number is negative, greater than 10^9 and unique is set to True
            or not an int.
    """
    ssn_length = 10 ** 9
    if type(number) is not int:
        raise ValueError(
            f"{number} is not an integer"
        )
    if number <= 0:
        raise ValueError(
            f"{number} is not a valid number (must be greater than 0)"
        )
    if unique:
        if number > ssn_length:
            raise ValueError(
                f"Number of unique SSN's requested {number} exceeds maximum possible unique values (1,0000,000)"
            )
        else:
            ssn_list = random.sample(population=range(ssn_length), k=number)
            for i in range(number):
                ssn_list[i] = int_to_ssn(x=ssn_list[i], dashes=dashes)
            return ssn_list
    else:
        ssn_list = random.choices(population=range(ssn_length), k=number)
        for i in range(number):
            ssn_list[i] = int_to_ssn(x=ssn_list[i], dashes=dashes)
        return ssn_list


def generate_strings(length=2, chars=string.digits):
    """Returns a generator for all combinations of strings of length length using characters specified in chars.

    Reference:
    https://stackoverflow.com/questions/43119744/python-generate-all-possible-strings-of-length-n

    Args:
        length (int): Length of individual string to be generated
        chars (str): String of characters to be used for cartesian product

    Yields:
        Generator[str]:
            A generator for all combinations of strings of length length using characters specified in chars.
    """
    #
    for item in itertools.product(chars, repeat=length):
        yield "".join(item)


def reservoir_sample(iterable, k):
    it = iter(iterable)
    if not (k > 0):
        raise ValueError("sample size must be positive")

    sample = list(itertools.islice(it, k))  # fill the reservoir
    random.shuffle(sample)  # if number of items less then *k* then
    #   return all items in random order.
    for i, item in enumerate(it, start=k + 1):
        j = random.randrange(i)  # random [0..i)
        if j < k:
            sample[j] = item  # replace item with gradually decreasing probability
    return sample


if __name__ == "__main__":
    # Testing/performance
    import timeit
    test_iterations = 1000

    print("Random SSN, 10, non-unique, w/ dashes")
    print(random_ssn(10))
    t = timeit.Timer(stmt="util.random_ssn(10)", setup="import util")
    print(f"Average runtime (n={test_iterations} times): %f\n" % t.timeit(test_iterations))

    print("Random SSN, 10, unique, w/ dashes")
    print(random_ssn(10, unique=True))
    t = timeit.Timer(stmt="util.random_ssn(10, unique=True)", setup="import util")
    print(f"Average runtime (n={test_iterations} times): %f\n" % t.timeit(test_iterations))

    print("Random SSN, 10, non-unique, w/o dashes")
    print(random_ssn(10, dashes=False))
    t = timeit.Timer(stmt="util.random_ssn(10, dashes=False)", setup="import util")
    print(f"Average runtime (n={test_iterations} times): %f\n" % t.timeit(test_iterations))

    print("Random SSN, 10, unique, w/o dashes")
    print(random_ssn(10, unique=True, dashes=False))
    t = timeit.Timer(stmt="util.random_ssn(10, unique=True, dashes=False)", setup="import util")
    print(f"Average runtime (n={test_iterations} times): %f" % t.timeit(test_iterations))
