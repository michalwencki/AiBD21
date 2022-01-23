import pytest
from cl_bubblesort import cl_bubblesort

def test_cl_bubblesort():
    unsorted_array = [4,3,19,2,6,8]
    want = [2,3,4,6,8,19]
    got = cl_bubblesort(unsorted_array)
    assert got == want
