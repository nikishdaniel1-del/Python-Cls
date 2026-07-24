import pytest
from sample import add

@pytest.mark.parametrize("operation,a,b,expected",[(add,2,6,8),(add,-2,-3,-5),(add,5,0,5),(add,-1,3,2)])

def test_operations(operation,a,b,expected):
    assert operation(a,b)==expected