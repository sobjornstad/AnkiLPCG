from itertools import zip_longest
import re
from typing import Any, Callable, Dict, Iterable, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from anki.notes import Note


class PoemLine:
    def __init__(self) -> None:
        self.predecessor = self  # so it's the right type...
        self.successor: Optional['PoemLine'] = None
        self.seq = -1

    def populate_note(self, note: 'Note', title: str, author: str, tags: List[str],
                      context_lines: int, recite_lines: int, deck_id: int) -> None:
        """
        Fill the _note_ with content testing on the current line.
        """
        note.note_type()['did'] = deck_id  # type: ignore
        note.tags = tags
        note['Title'] = title
        note['Author'] = author
        note['Sequence'] = str(self.seq)
        note['Context'] = self._format_context(context_lines)
        note['Line'] = self._format_text(recite_lines)
        prompt = self._get_prompt(recite_lines)
        if prompt is not None:
            note['Prompt'] = prompt

    def _format_context(self, context_lines: int):
        return ''.join("<p>%s</p>" % i for i in self._get_context(context_lines))

    def _format_text(self, recitation_lines: int):
        return ''.join("<p>%s</p>" % i for i in self._get_text(recitation_lines))

    def _get_context(self, _lines: int, _recursing=False) -> List[str]:
        """
        Return a list of context lines, including the current line and
        (lines - 1) of its predecessors.
        """
        raise NotImplementedError

    def _get_text(self, _lines: int) -> List[str]:
        """
        Return a list of recitation lines, including the current line and
        (lines - 1) of its successors.
        """
        raise NotImplementedError

    def _get_prompt(self, configured_recitation_lines: int) -> Optional[str]:
        """
        Return a prompt string to be shown on the question side after the
        lines of context, or None to use the template default of [...]. This
        is currently used to let the user know how many lines to recite, but
        could plausibly be used for other things as well in the future.
        """
        raise NotImplementedError


class Beginning(PoemLine):
    """
    A dummy node indicating the beginning of the poem. It's included only so
    it can polymorphically have its context and sequence retrieved.
    Attempting to do anything else with the node is an error.
    """
    def __init__(self):
        super().__init__()
        self.seq = 0
        self.text = "[Beginning]"

    def _get_context(self, _lines: int, _recursing=False) -> List[str]:
        return [self.text]

    def _get_text(self, _lines: int) -> List[str]:
        """
        The Beginning node has no defined successors, as it's not a line
        we'll ever be asked to recite and thus we never need to know what its
        text property is -- the first line we would ever be asked to recite
        would be the following line.
        """
        raise NotImplementedError

    def populate_note(self, note: 'Note', title: str, author: str, tags: List[str],
                      context_lines: int, recite_lines: int, deck_id: int) -> None:
        raise AssertionError("The Beginning node cannot be used to populate a note.")


class SingleLine(PoemLine):
    """
    A single line in a typical poem. It has text, a sequence number, a
    predecessor (possibly the Beginning node, but never None), and if it's
    not the last line of the poem, a successor.
    """
    def __init__(self, text: str, predecessor: 'PoemLine') -> None:
        super().__init__()
        self.text = text
        self.predecessor = predecessor
        self.seq = self.predecessor.seq + 1

    def _get_context(self, lines: int, recursing=False) -> List[str]:
        if lines == 0:
            return [self.text]
        elif not recursing:
            return self.predecessor._get_context(lines - 1, True)
        else:
            return self.predecessor._get_context(lines - 1, True) + [self.text]

    def _get_text(self, lines: int) -> List[str]:
        if lines == 1 or self.successor is None:
            return [self.text]
        else:
            return [self.text] + self.successor._get_text(lines - 1)

    def _get_prompt(self, configured_recitation_lines: int) -> Optional[str]:
        # It's important to calculate the lines_to_recite for _this_ instance
        # instead of just getting the configuration parameter, as if we're at
        # the end it may be fewer.
        lines_to_recite = len(self._get_text(configured_recitation_lines))
        if lines_to_recite == 1:
            return None
        else:
            return f"[...{lines_to_recite}]"


class GroupedLine(PoemLine):
    r"""
    A virtual "line" in a poem that has grouping set, so that multiple short
    lines can be treated as one line by LPCG. It consists of multiple text lines.

    The difference between grouped lines and ordinary lines with double the
    context and recitation values is that there is no overlapping. So this with
    default context and recitation values and a group of 2 yields only 3 notes,
    whereas a context of 4 and recitation of 2 would result in 6 notes:

        /A
        \B
        /C
        \D
        /E
        \F
    """
    def __init__(self, text: List[str], predecessor: 'PoemLine') -> None:
        super().__init__()
        self.text_lines = text
        self.predecessor = predecessor
        self.seq = self.predecessor.seq + 1

    def _get_context(self, lines: int, recursing=False) -> List[str]:
        if lines == 0:
            return self.text_lines
        elif not recursing:
            return self.predecessor._get_context(lines - 1, True)
        else:
            return self.predecessor._get_context(lines - 1, True) + self.text_lines

    def _get_text(self, lines: int) -> List[str]:
        if lines == 1 or self.successor is None:
            return self.text_lines
        else:
            return self.text_lines + self.successor._get_text(lines - 1)

    def _get_prompt(self, configured_recitation_lines: int) -> Optional[str]:
        lines_to_recite = len(self._get_text(configured_recitation_lines))
        if lines_to_recite == 1:
            return None
        else:
            return f"[...{lines_to_recite}]"


def groups_of_n(iterable: Iterable, n: int) -> Iterable:
    """
    s -> (s0,s1,s2,...sn-1), (sn,sn+1,sn+2,...s2n-1), (s2n,s2n+1,s2n+2,...s3n-1), ...

    Credit: https://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
    """
    return zip_longest(*[iter(iterable)]*n)


def _poemlines_from_textlines(text_lines: List[str], group_lines: int) -> List[PoemLine]:
    """
    Given a list of cleansed text lines, create a list of PoemLine objects
    from it. These are each capable of constructing a correct note testing
    themselves when the to_note() method is called on them.
    """
    beginning = Beginning()
    lines: List[PoemLine] = []  # does not include beginning, as it's not actually a line
    pred: PoemLine = beginning
    poem_line: PoemLine

    if group_lines == 1:
        for text_line in text_lines:
            poem_line = SingleLine(text_line, pred)
            lines.append(poem_line)
            pred.successor = poem_line
            pred = poem_line
    else:
        for line_set in groups_of_n(text_lines, group_lines):
            poem_line = GroupedLine([i for i in line_set if i is not None], pred)
            lines.append(poem_line)
            pred.successor = poem_line
            pred = poem_line
    return lines


def cleanse_text(string: str, config: Dict[str, Any]) -> List[str]:
    """
    Munge raw text from the poem editor into a list of lines that can be
    directly made into notes.
    """
    def _normalize_blank_lines(text_lines):
        # remove consecutive lone newlines
        new_text = []
        last_line = ""
        for i in text_lines:
            if last_line.strip() or i.strip():
                new_text.append(i)
            last_line = i
        # remove lone newlines at beginning and end
        for i in (0, -1):
            if not new_text[i].strip():
                del new_text[i]
        return new_text

    text = string.splitlines()
    # record a level of indentation if appropriate
    text = [re.sub(r'^[ \t]+', r'<indent>', i) for i in text]
    # remove comments and normalize blank lines
    text = [i.strip() for i in text if not i.startswith("#")]
    text = [re.sub(r'\s*\#.*$', '', i) for i in text]
    text = _normalize_blank_lines(text)
    # add end-of-stanza/poem markers where appropriate
    for i in range(len(text)):
        if i == len(text) - 1:
            text[i] += config['endOfTextMarker']
        elif not text[i+1].strip():
            text[i] += config['endOfStanzaMarker']
    # entirely remove all blank lines
    text = [i for i in text if i.strip()]
    # replace <indent>s with valid CSS
    text = [re.sub(r'^<indent>(.*)$', r'<span class="indent">\1</span>', i)
            for i in text]
    return text


def add_notes(col: Any, note_constructor: Callable,
              title: str, author:str, tags: List[str], text: List[str],
              deck_id: int, context_lines: int, group_lines: int, 
              recite_lines: int):
    """
    Generate notes from the given title, author, tags, poem text, and number of
    lines of context. Return the number of notes added.

    Return the number of notes added.

    Raises KeyError if the note type is missing fields, which I've seen
    happen a couple times when users accidentally edited the note type. The
    caller should offer an appropriate error message in this case.
    """
    added = 0
    for line in _poemlines_from_textlines(text, group_lines):
        n = note_constructor(col, col.models.by_name("LPCG 1.0"))
        line.populate_note(n, title, author, tags, context_lines, recite_lines, deck_id)
        col.addNote(n)
        added += 1
    return added
