import numpy as np
import string
import itertools
import random


def random_ssn(number: int = 1, unique: bool = False):
    """
    Return a random SSN or list of SSN's

    :param number: Number of SSN's to return. If blank, None or 1, a single string will be returned. Default: None
    :param unique: Boolean indicating if returned SSN's should be unique.
    :return: SSN string or list of SSN strings.
    :rtype: str or list[str]
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


# Reference:
# https://stackoverflow.com/questions/43119744/python-generate-all-possible-strings-of-length-n
def generate_strings(length=2, chars=string.digits):
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
