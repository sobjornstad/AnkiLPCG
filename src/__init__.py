"""
LPCG - Lyrics/Poetry Cloze Generator
version 1.2.1
Copyright (c) 2016-2019 Soren Bjornstad <contact@sorenbjornstad.com>
License: GNU AGPL, version 3 or later: <http://www.gnu.org/licenses/agpl.html>
"""

# pylint: disable=import-error, no-name-in-module
# pylint: disable=invalid-name
import codecs
import itertools
import re

from PyQt5.QtWidgets import QDialog
import aqt
from aqt.qt import QAction
from aqt.utils import getFile, showWarning, askUser, tooltip

from . import import_dialog as lpcg_form
from . import model_data as lpcg_models
from .gen_notes import add_notes, process_text


class LPCGDialog(QDialog):
    """
    Import Lyrics/Poetry dialog, the core of the add-on. The user can either
    enter the text of a poem in the editor or import a text file from somewhere
    else on the computer. The poem can be entered with usual markup (blank
    lines between stanzas, one level of indentation with tabs or spaces in
    front of lines). LPCG then processes it into notes with two lines of
    context and adds them to the user's collection.
    """

    def __init__(self, mw):
        self.mw = mw

        QDialog.__init__(self)
        self.form = lpcg_form.Ui_Dialog()
        self.form.setupUi(self)
        self.deckChooser = aqt.deckchooser.DeckChooser(
            self.mw, self.form.deckChooser)

        self.form.addCardsButton.clicked.connect(self.accept)
        self.form.cancelButton.clicked.connect(self.reject)
        self.form.openFileButton.clicked.connect(self.onOpenFile)

    def accept(self):
        "On close, create notes from the contents of the poem editor."
        title = self.form.titleBox.text().strip()
        tags = self.mw.col.tags.split(self.form.tagsBox.text())
        text = process_text(self.form.textBox.toPlainText().strip(),
                            self.mw.addonManager.getConfig(__name__))
        context_lines = self.form.contextLinesSpin.value()
        recite_lines = self.form.reciteLinesSpin.value()
        group_lines = self.form.groupLinesSpin.value()
        did = self.deckChooser.selectedId()

        if not title.strip():
            showWarning("You must enter a title for this poem.")
            return
        if self.mw.col.findNotes(f'"note:{lpcg_models.NAME}" "Title:{title}"'):
            showWarning("You already have a poem by that title in your "
                        "database. Please check to see if you've already "
                        "added it, or use a different name.")
            return
        if not text:
            showWarning("There's nothing to generate cards from! "
                        "Please type a poem in the box, or use the "
                        '"open file" button to import a text file.')
            return

        notes_generated = add_notes(self.mw.col, title, tags, text, did, context_lines)
        if notes_generated:
            super(LPCGDialog, self).accept()
            self.mw.reset()
            tooltip("%i notes added." % notes_generated)

    def onOpenFile(self):
        """
        Read a text file (in UTF-8 encoding) and replace the contents of the
        poem editor with the contents of the file.
        """
        if (self.form.textBox.toPlainText().strip()
                and not askUser("Importing a file will replace the current "
                                "contents of the poem editor. Continue?")):
            return
        filename = getFile(self, "Import file", None, key="import")
        if not filename: # canceled
            return
        with codecs.open(filename, 'r', 'utf-8') as f:
            text = f.read()
        self.form.textBox.setPlainText(text)


def ensure_note_type():
    "Create the LPCG note type if it doesn't already exist."
    mm = aqt.mw.col.models
    model = mm.byName(lpcg_models.NAME)
    if model is not None:
        # Inject night-mode update if not present.
        if '.nightMode .cloze' not in model['css']:
            model['css'] += ("\n\n" + lpcg_models.NIGHTMODE_CLOZE)
        
        # In any case, don't recreate the note type.
        return

    model = mm.new(lpcg_models.NAME)
    for i in lpcg_models.FIELDS:
        field = mm.newField(i)
        mm.addField(model, field)
    t = mm.newTemplate(lpcg_models.TEMPLATE_NAME)
    t['qfmt'] = lpcg_models.FRONT_TEMPLATE
    t['afmt'] = lpcg_models.BACK_TEMPLATE
    mm.addTemplate(model, t)
    model['css'] = lpcg_models.STYLING
    model['sortf'] = lpcg_models.SORT_FIELD
    mm.add(model)


def open_dialog():
    "Launch the add-poem dialog."
    dialog = LPCGDialog(aqt.mw)
    dialog.exec_()


action = QAction(aqt.mw)
action.setText("Import &Lyrics/Poetry")
aqt.mw.form.menuTools.addAction(action)
action.triggered.connect(open_dialog)

addHook('profileLoaded', ensure_note_type)
