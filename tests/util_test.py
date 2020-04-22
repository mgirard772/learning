import src
import pytest
import re
import string
import mock


def test_int_to_ssn_dash():
    actual = [src.int_to_ssn(1, dashes=True), src.int_to_ssn(1, dashes=False)]
    expected = ["000-00-0001", "000000001"]
    assert actual == expected


def test_int_to_ssn_float():
    with pytest.raises(ValueError):
        src.int_to_ssn(123.4)


def test_int_to_ssn_range():
    with pytest.raises(ValueError):
        src.int_to_ssn(-1)


def test_random_ssn():
    result = src.random_ssn(1, True, False) + src.random_ssn(1, False, True)
    assert re.match(r"\d{3}-\d{2}-\d{4}", result[0]) and re.match(r"\d{9}", result[1])

def test_random_ssn_float():
    with pytest.raises(ValueError):
        src.random_ssn(1.5, True, False)


def test_random_ssn_max():
    with pytest.raises(ValueError):
        src.random_ssn(10**9+1, True, True)


def test_random_ssn_neg():
    with pytest.raises(ValueError):
        src.random_ssn(-1, True, True)


def test_gen_strings():
    assert list(src.generate_strings(2, string.digits)).__len__() == 100


def test_reservoir_sample():
    assert src.reservoir_sample([x for x in range(1, 100)], 10).__len__() == 10


def test_reservoir_sample_error():
    with pytest.raises(ValueError):
        src.reservoir_sample([x for x in range(1, 100)], -1)
