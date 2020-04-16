import string
import itertools
import random


def random_ssn(number: int = 1, unique: bool = False):
    """
    Return a random SSN or list of SSN's

    Args:
        number (int): Number of SSN's to return. If blank, None or 1, a single string will be returned. (default is 1)
        unique (boolean): Boolean indicating if returned SSN's should be unique. (default is False)

    Returns:
        List[str]: An SSN string or list of SSN strings
    """
    ssn_length = 10 ** 9
    if number is None or number == 1:
        temp_string = str(random.randrange(10**9))
        temp_string = "0"*(9-temp_string.__len__())+temp_string
        temp_string = "%s-%s-%s" % (temp_string[0:3], temp_string[3:5], temp_string[5:9])
        return temp_string
    else:
        if unique:
            if number > ssn_length:
                raise ValueError(
                    "Number of unique SSN's requested (%d) exceeds maximum possible unique values (1,0000,000)" % (
                        number))
            else:
                # result_tuples = list(map(lambda x,y:(x,y), range(number), random.sample(range(ssn_length), number)))
                ssn_gen = generate_strings(9, string.digits)
                # Resevoir Sampling
                # Reference: https://stackoverflow.com/questions/32788380/python-choose-random-line-from-file-then-delete-that-line/32792504#32792504
                result = list(itertools.islice(ssn_gen, number))
                result_status = [False] * number
                for index, datum in enumerate(ssn_gen, start=number + 1):
                    j = random.randrange(index)
                    if j < number:  # [0,i)
                        result[j] = "%s-%s-%s" % (datum[0:3], datum[3:5], datum[5:9])
                        result_status[j] = True
                        if sum(result_status) == number:
                            break
                return result
        else:
            temp_list = [random_ssn(1) for x in range(0, number)]
            return temp_list


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
    #Testing/performance
    import timeit
    print(random_ssn(None))
    print("Random SSN, 20, non-unique")
    print(random_ssn(20))
    t = timeit.Timer(stmt="lu.random_ssn(20)", setup="import learning_util as lu")
    print("Average runtime (n=1000 times): %f" % t.timeit(1000))
