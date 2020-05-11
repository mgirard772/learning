import pytest
import itertools

def pytest_addoption(parser):
    parser.addoption("--smoke", action="store_true", help="run additional smoke testing")

def pytest_generate_tests(metafunc):
    if "test_param" in metafunc.fixturenames:
        if metafunc.config.getoption("smoke"):
            values = list(range(-3, 5))
            metafunc.parametrize("test_param", values)
        else:
            metafunc.parametrize("test_param", [])
