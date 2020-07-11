from textwrap import dedent
from typing import Sequence

import pytest

# pylint: disable=unused-wildcard-import
from src.gen_notes import *


MOCK_CONFIG = {'endOfTextMarker': 'X', 'endOfStanzaMarker': 'Y'}
INDENT_HTML_START = '<span class="indent">'
INDENT_HTML_END = '</span>'


@pytest.mark.parametrize("n,expected", [
    (2, ((1, 2), (3, 4), (5, 6))),
    (3, ((1, 2, 3), (4, 5, 6))),
    (4, ((1, 2, 3, 4), (5, 6, None, None))),
])
def test_groups_of_n(n: int, expected: Sequence[int]):
    original_iterable = (1, 2, 3, 4, 5, 6)
    grouped = groups_of_n(original_iterable, n)
    for actual, exp in zip(grouped, expected):
        assert actual == exp


class TestCleanseText:
    def test_cleanse(self):
        limerick = dedent("""
        # Ulrich Neisser
        You can get a good deal from rehearsal
        If it just has the proper dispersal.   

          You would just be an ass
          To do it en masse,
        Your remembering would turn out much worsal.
        """).strip()
        result = cleanse_text(limerick, MOCK_CONFIG)

        assert result[0] == "You can get a good deal from rehearsal"
        assert result[1] == "If it just has the proper dispersal.Y"
        assert result[2] == f"{INDENT_HTML_START}You would just be an ass{INDENT_HTML_END}"
        assert result[3] == f"{INDENT_HTML_START}To do it en masse,{INDENT_HTML_END}"
        assert result[4] == "Your remembering would turn out much worsal.X"


    def test_cleanse_multiple_blank_lines(self):
        test_case = dedent("""
        # This has lots of blank lines and comments that could mess things up.
        Here is a first line


        And here is a second line.
        And a third line.
        # Now a comment

        # And another comment

        And here, at last, is the end of the poem.
        """).strip()
        result = cleanse_text(test_case, MOCK_CONFIG)

        assert result[0] == "Here is a first lineY"
        assert result[1] == "And here is a second line."
        assert result[2] == "And a third line.Y"
        assert result[3] == "And here, at last, is the end of the poem.X"


    def test_unequal_indentation(self):
        limerick = dedent("""
        # Ulrich Neisser
        You can get a good deal from rehearsal
        If it just has the proper dispersal.   

        	You would just be an ass
           To do it en masse,
        Your remembering would turn out much worsal.
        """).strip()
        result = cleanse_text(limerick, MOCK_CONFIG)

        assert result[0] == "You can get a good deal from rehearsal"
        assert result[1] == "If it just has the proper dispersal.Y"
        assert result[2] == f"{INDENT_HTML_START}You would just be an ass{INDENT_HTML_END}"
        assert result[3] == f"{INDENT_HTML_START}To do it en masse,{INDENT_HTML_END}"
        assert result[4] == "Your remembering would turn out much worsal.X"

    
    def test_line_comment(self):
        limerick = dedent("""
        Here is a line # with a comment
        And a second line.
        """).strip()
        result = cleanse_text(limerick, MOCK_CONFIG)

        assert result[0] == "Here is a line"
        assert result[1] == "And a second line.X"
    