import pytest


@pytest.hookimpl(wrapper=True)
def pytest_pyfunc_call(pyfuncitem, nextitem):

    # check things here

    return (yield)
