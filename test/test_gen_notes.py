from textwrap import dedent
from typing import Sequence

import pytest

# pylint: disable=unused-wildcard-import
from src.gen_notes import *


MOCK_CLEANSE_CONFIG = {'endOfTextMarker': 'X', 'endOfStanzaMarker': 'Y'}
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
        result = cleanse_text(limerick, MOCK_CLEANSE_CONFIG)

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
        """).strip() + "\n\n"
        result = cleanse_text(test_case, MOCK_CLEANSE_CONFIG)

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
        result = cleanse_text(limerick, MOCK_CLEANSE_CONFIG)

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
        result = cleanse_text(limerick, MOCK_CLEANSE_CONFIG)

        assert result[0] == "Here is a line"
        assert result[1] == "And a second line.X"
    

test_poem = dedent("""
    # Samuel Longfellow
    'Tis winter now; the fallen snow
    Has left the heavens all coldly clear;
    Through leafless boughs the sharp winds blow,
    And all the earth lies dead and drear.

    And yet God's love is not withdrawn;
    His life within the keen air breathes;
    God's beauty paints the crimson dawn,
    And clothes the boughs with glittering wreaths.

    And though abroad the sharp winds blow,
    And skies are chill, and frosts are keen,
    Home closer draws her circle now,
    And warmer glows her light within.

    O God! Who gives the winter's cold
    As well as summer's joyous rays,
    Us warmly in Thy love enfold,
    And keep us through life's wintry days.
    """).strip()


class MockModel:
    def __init__(self):
        self.properties = {}

    def __call__(self):
        return self.properties

    def byName(self, name):
        return self


class MockCollection:
    def __init__(self):
        self.notes = []

    def addNote(self, note):
        self.notes.append(note)

    @property
    def models(self):
        return MockModel()


class MockNote:
    def __init__(self, collection, model):
        self.collection = collection
        self.model = model
        self.tags = []
        self.properties = {}

    def __getitem__(self, item):
        return self.properties[item]

    def __setitem__(self, item, value):
        self.properties[item] = value

    def __delitem__(self, item):
        del self.properties[item]

    def __contains__(self, item):
        return item in self.properties


@pytest.fixture
def mock_note():
    col = MockCollection()
    note_constructor = MockNote
    title = "'Tis Winter"
    tags = ["poem", "test"]
    deck_id = 1
    context_lines = 2
    recite_lines = 1
    group_lines = 1
    text = cleanse_text(test_poem, MOCK_CLEANSE_CONFIG)
    return dict(locals())


def test_render_default_settings(mock_note):
    col = mock_note['col']
    num_added = add_notes(**mock_note)

    assert num_added == 16
    assert len(col.notes) == 16

    assert col.notes[0]['Title'] == mock_note['title']
    assert col.notes[0].tags == mock_note['tags']
    assert col.notes[0]['Sequence'] == "1"
    assert col.notes[0]['Context'] == "<p>[Beginning]</p>"
    assert col.notes[0]['Line'] == "<p>'Tis winter now; the fallen snow</p>"
    assert 'Prompt' not in col.notes[0]

    assert col.notes[3]['Title'] == mock_note['title']
    assert col.notes[3].tags == mock_note['tags']
    assert col.notes[3]['Sequence'] == "4"
    assert col.notes[3]['Context'] == (
        "<p>Has left the heavens all coldly clear;</p>"
        "<p>Through leafless boughs the sharp winds blow,</p>"
    )
    assert col.notes[3]['Line'] == "<p>And all the earth lies dead and drear.Y</p>"
    assert 'Prompt' not in col.notes[3]


### GROUPS ###
def test_render_groups_of_two(mock_note):
    col = mock_note['col']
    mock_note['group_lines'] = 2
    num_added = add_notes(**mock_note)

    assert num_added == 8
    assert len(col.notes) == 8

    # We won't bother testing title and tags for further items.
    assert col.notes[0]['Sequence'] == "1"
    assert col.notes[0]['Context'] == "<p>[Beginning]</p>"
    assert col.notes[0]['Line'] == (
        "<p>'Tis winter now; the fallen snow</p>"
        "<p>Has left the heavens all coldly clear;</p>"
    )
    assert col.notes[0]['Prompt'] == "[...2]"

    assert col.notes[1]['Sequence'] == "2"
    assert col.notes[1]['Context'] == (
        "<p>[Beginning]</p>"
        "<p>'Tis winter now; the fallen snow</p>"
        "<p>Has left the heavens all coldly clear;</p>"
    )
    assert col.notes[1]['Line'] == (
        "<p>Through leafless boughs the sharp winds blow,</p>"
        "<p>And all the earth lies dead and drear.Y</p>"
    )
    assert col.notes[1]['Prompt'] == "[...2]"


def test_render_groups_of_three(mock_note):
    col = mock_note['col']
    mock_note['group_lines'] = 3
    num_added = add_notes(**mock_note)

    assert num_added == 6
    assert len(col.notes) == 6

    assert col.notes[0]['Title'] == mock_note['title']
    assert col.notes[0].tags == mock_note['tags']
    assert col.notes[0]['Sequence'] == "1"
    assert col.notes[0]['Context'] == "<p>[Beginning]</p>"
    assert col.notes[0]['Line'] == (
        "<p>'Tis winter now; the fallen snow</p>"
        "<p>Has left the heavens all coldly clear;</p>"
        "<p>Through leafless boughs the sharp winds blow,</p>"
    )
    assert col.notes[0]['Prompt'] == "[...3]"

    # Last item has six lines of context but only one recitation line, with no prompt
    # (as 16 % 3 = 1).
    assert col.notes[5]['Sequence'] == "6"
    assert col.notes[5]['Context'] == (
        "<p>And skies are chill, and frosts are keen,</p>"
        "<p>Home closer draws her circle now,</p>"
        "<p>And warmer glows her light within.Y</p>"
        "<p>O God! Who gives the winter's cold</p>"
        "<p>As well as summer's joyous rays,</p>"
        "<p>Us warmly in Thy love enfold,</p>"
    )
    assert col.notes[5]['Line'] == "<p>And keep us through life's wintry days.X</p>"
    assert 'Prompt' not in col.notes[5], col.notes[5]['Prompt']


### CONTEXT LINES ###
def test_render_three_context_lines(mock_note):
    col = mock_note['col']
    mock_note['context_lines'] = 3
    num_added = add_notes(**mock_note)

    assert num_added == 16
    assert len(col.notes) == 16

    assert col.notes[0]['Sequence'] == "1"
    assert col.notes[0]['Context'] == "<p>[Beginning]</p>"
    assert col.notes[0]['Line'] == "<p>'Tis winter now; the fallen snow</p>"
    assert 'Prompt' not in col.notes[0]

    assert col.notes[1]['Context'] == (
        "<p>[Beginning]</p>"
        "<p>'Tis winter now; the fallen snow</p>"
    )
    assert col.notes[1]['Line'] == "<p>Has left the heavens all coldly clear;</p>"

    assert col.notes[2]['Context'] == (
        "<p>[Beginning]</p>"
        "<p>'Tis winter now; the fallen snow</p>"
        "<p>Has left the heavens all coldly clear;</p>"
    )
    assert col.notes[2]['Line'] == "<p>Through leafless boughs the sharp winds blow,</p>"

    assert col.notes[3]['Context'] == (
        "<p>'Tis winter now; the fallen snow</p>"
        "<p>Has left the heavens all coldly clear;</p>"
        "<p>Through leafless boughs the sharp winds blow,</p>"
    )
    assert col.notes[3]['Line'] == "<p>And all the earth lies dead and drear.Y</p>"

    assert col.notes[4]['Context'] == (
        "<p>Has left the heavens all coldly clear;</p>"
        "<p>Through leafless boughs the sharp winds blow,</p>"
        "<p>And all the earth lies dead and drear.Y</p>"
    )
    assert col.notes[4]['Line'] == "<p>And yet God's love is not withdrawn;</p>"


### RECITATION LINES ###
def test_render_two_recitation_lines(mock_note):
    col = mock_note['col']
    mock_note['recite_lines'] = 2
    num_added = add_notes(**mock_note)

    # Unlike grouping, having more recitation lines involves overlap,
    # so there are still 16 notes.
    assert num_added == 16
    assert len(col.notes) == 16

    assert col.notes[0]['Context'] == "<p>[Beginning]</p>"
    assert col.notes[0]['Line'] == (
        "<p>'Tis winter now; the fallen snow</p>"
        "<p>Has left the heavens all coldly clear;</p>"
    )
    assert col.notes[0]['Prompt'] == "[...2]"

    assert col.notes[1]['Context'] == (
        "<p>[Beginning]</p>"
        "<p>'Tis winter now; the fallen snow</p>"
    )
    assert col.notes[1]['Line'] == (
        "<p>Has left the heavens all coldly clear;</p>"
        "<p>Through leafless boughs the sharp winds blow,</p>"
    )

    assert col.notes[2]['Context'] == (
        "<p>'Tis winter now; the fallen snow</p>"
        "<p>Has left the heavens all coldly clear;</p>"
    )
    assert col.notes[2]['Line'] == (
        "<p>Through leafless boughs the sharp winds blow,</p>"
        "<p>And all the earth lies dead and drear.Y</p>"
    )

    # The very last line will request a single recitation.
    assert col.notes[-1]['Context'] == (
        "<p>As well as summer's joyous rays,</p>"
        "<p>Us warmly in Thy love enfold,</p>"
    )
    assert col.notes[-1]['Line'] == "<p>And keep us through life's wintry days.X</p>"
    assert 'Prompt' not in col.notes[-1]


### TRIPLE PLAY ###
def test_render_increase_all_options(mock_note):
    """
    In this configuration, we have lines grouped into sets of 2 -- so 8
    virtual lines -- and then we show 3 virtual lines as context (6 physical
    lines) and request 2 virtual lines for recitation (4 physical lines).
    """
    col = mock_note['col']
    mock_note['context_lines'] = 3
    mock_note['recite_lines'] = 2
    mock_note['group_lines'] = 2
    num_added = add_notes(**mock_note)

    # Only grouping reduces the number; the other parameters cause only
    # additional overlap.
    assert num_added == 8
    assert len(col.notes) == 8

    assert col.notes[0]['Context'] == "<p>[Beginning]</p>"
    assert col.notes[0]['Line'] == (
        "<p>'Tis winter now; the fallen snow</p>"
        "<p>Has left the heavens all coldly clear;</p>"
        "<p>Through leafless boughs the sharp winds blow,</p>"
        "<p>And all the earth lies dead and drear.Y</p>"
    )
    assert col.notes[0]['Prompt'] == "[...4]"

    assert col.notes[1]['Context'] == (
        "<p>[Beginning]</p>"
        "<p>'Tis winter now; the fallen snow</p>"
        "<p>Has left the heavens all coldly clear;</p>"
    )
    assert col.notes[1]['Line'] == (
        "<p>Through leafless boughs the sharp winds blow,</p>"
        "<p>And all the earth lies dead and drear.Y</p>"
        "<p>And yet God's love is not withdrawn;</p>"
        "<p>His life within the keen air breathes;</p>"
    )
    assert col.notes[1]['Prompt'] == "[...4]"

    assert col.notes[2]['Context'] == (
        "<p>[Beginning]</p>"
        "<p>'Tis winter now; the fallen snow</p>"
        "<p>Has left the heavens all coldly clear;</p>"
        "<p>Through leafless boughs the sharp winds blow,</p>"
        "<p>And all the earth lies dead and drear.Y</p>"
    )
    assert col.notes[2]['Line'] == (
        "<p>And yet God's love is not withdrawn;</p>"
        "<p>His life within the keen air breathes;</p>"
        "<p>God's beauty paints the crimson dawn,</p>"
        "<p>And clothes the boughs with glittering wreaths.Y</p>"
    )
    assert col.notes[2]['Prompt'] == "[...4]"

    assert col.notes[3]['Context'] == (
        "<p>'Tis winter now; the fallen snow</p>"
        "<p>Has left the heavens all coldly clear;</p>"
        "<p>Through leafless boughs the sharp winds blow,</p>"
        "<p>And all the earth lies dead and drear.Y</p>"
        "<p>And yet God's love is not withdrawn;</p>"
        "<p>His life within the keen air breathes;</p>"
    )
    assert col.notes[3]['Line'] == (
        "<p>God's beauty paints the crimson dawn,</p>"
        "<p>And clothes the boughs with glittering wreaths.Y</p>"
        "<p>And though abroad the sharp winds blow,</p>"
        "<p>And skies are chill, and frosts are keen,</p>"
    )
    assert col.notes[3]['Prompt'] == "[...4]"

    assert col.notes[6]['Context'] == (
        "<p>God's beauty paints the crimson dawn,</p>"
        "<p>And clothes the boughs with glittering wreaths.Y</p>"
        "<p>And though abroad the sharp winds blow,</p>"
        "<p>And skies are chill, and frosts are keen,</p>"
        "<p>Home closer draws her circle now,</p>"
        "<p>And warmer glows her light within.Y</p>"
    )
    assert col.notes[6]['Line'] == (
        "<p>O God! Who gives the winter's cold</p>"
        "<p>As well as summer's joyous rays,</p>"
        "<p>Us warmly in Thy love enfold,</p>"
        "<p>And keep us through life's wintry days.X</p>"
    )
    assert col.notes[6]['Prompt'] == "[...4]"

    assert col.notes[7]['Context'] == (
        "<p>And though abroad the sharp winds blow,</p>"
        "<p>And skies are chill, and frosts are keen,</p>"
        "<p>Home closer draws her circle now,</p>"
        "<p>And warmer glows her light within.Y</p>"
        "<p>O God! Who gives the winter's cold</p>"
        "<p>As well as summer's joyous rays,</p>"
    )
    assert col.notes[7]['Line'] == (
        "<p>Us warmly in Thy love enfold,</p>"
        "<p>And keep us through life's wintry days.X</p>"
    )
    assert col.notes[7]['Prompt'] == "[...2]"
