import pytest

# pylint: disable=unused-wildcard-import
from src.gen_notes import *

def test_groups_of_n():
    L = list(groups_of_n((1, 2, 3, 4, 5, 6), 2))
    assert L[0] == (1, 2)
    assert L[1] == (3, 4)
    assert L[2] == (5, 6)
