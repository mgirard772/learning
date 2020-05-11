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
    if 'num_runs' in metafunc.fixturenames:
        num_runs_set = range(1, 2)
        num_users_set = range(1, 4)
        num_updates_set = range(1, 3)
        parameter_set = [
            pytest.param(num_runs, num_users, num_updates) for num_runs, num_users, num_updates in
            itertools.product(num_runs_set, num_users_set, num_updates_set)
        ]
        metafunc.parametrize("num_runs,num_users,num_updates", parameter_set)
