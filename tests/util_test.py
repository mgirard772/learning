from src import util

def test_int_to_ssn():
    assert util.int_to_ssn(123121234, dashes=True) == "123-12-1234"