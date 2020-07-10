import re
from typing import Any, Dict, List

from anki.notes import Note

from . import model_data as lpcg_models


def process_text(string: str, config: Dict[str, Any]) -> List[str]:
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
    text = [re.sub(r'\#.*$', '', i) for i in text]
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


def add_notes(col: Any, title: str, tags: List[str], text: str, did: int,
              lines_of_context: int = 2):
    """
    Generate notes from the given title, tags, poem text, and number of
    lines of context. Return the number of notes added.
    """
    def newNote(seq: int, contexts: List[str], line: str) -> None:
        n = Note(col, col.models.byName(lpcg_models.NAME))
        n.model()['did'] = did
        n.tags = tags
        n['Title'] = title
        n['Sequence'] = str(seq)
        n['Context'] = ''.join("<p>%s</p>" % i for i in contexts)
        n['Line'] = line
        col.addNote(n)

    try:
        newNote(1, ["[First Line]"], text[0])
    except KeyError as e:
        showWarning(
            "The field {field} was not found on the {name} note type"
            " in your collection. If you don't have any LPCG notes"
            " yet, you can delete the note type in Tools -> Manage"
            " Note Types and restart Anki to fix this problem."
            " Otherwise, please add the field back to the note type. "
            .format(field=str(e), name=lpcg_models.NAME))
        return
    # loop for early lines that can't have all the context
    for seq in range(2, min(lines_of_context+1, len(text)+1)):
        newNote(seq, ["[Beginning]"] + text[0:seq-1], text[seq-1])
    # and for the rest
    for seq in range(lines_of_context+1, len(text)+1):
        newNote(seq, text[seq-lines_of_context-1:seq-1], text[seq-1])
    return seq
