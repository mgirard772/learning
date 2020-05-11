import pytest
import src

def test_int_to_ssn_smoke(test_param):
    try:
        if test_param < 0:
            with pytest.raises(ValueError):
                src.int_to_ssn(test_param)
        else:
            src.int_to_ssn(test_param)
            assert True
    except Exception:
        assert False
