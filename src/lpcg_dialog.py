import codecs

from PyQt5.QtWidgets import QDialog  # pylint: disable=no-name-in-module

import aqt
from aqt.qt import QAction  # pylint: disable=no-name-in-module
from aqt.utils import getFile, showWarning, askUser, tooltip

from . import import_dialog as lpcg_form
from .gen_notes import add_notes, process_text
from . import model_data as lpcg_models


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

        if not title:
            showWarning("You must enter a title for this poem.")
            return
        if self.mw.col.findNotes(f'"note:{lpcg_models.NAME}" "Title:{title}"'):
            showWarning("You already have a poem by that title in your "
                        "database. Please check to see if you've already "
                        "added it, or use a different name.")
            return
        if not self.form.textBox.toPlainText().strip():
            showWarning("There's nothing to generate cards from! "
                        "Please type a poem in the box, or use the "
                        '"Open File" button to import a text file.')
            return

        tags = self.mw.col.tags.split(self.form.tagsBox.text())
        text = process_text(self.form.textBox.toPlainText().strip(),
                            self.mw.addonManager.getConfig(__name__))
        context_lines = self.form.contextLinesSpin.value()
        recite_lines = self.form.reciteLinesSpin.value()
        group_lines = self.form.groupLinesSpin.value()
        did = self.deckChooser.selectedId()

        try:
            notes_generated = add_notes(self.mw.col, title, tags, text, did,
                                        context_lines, group_lines, recite_lines)
        except KeyError as e:
            showWarning(
                "The field {field} was not found on the {name} note type"
                " in your collection. If you don't have any LPCG notes"
                " yet, you can delete the note type in Tools -> Manage"
                " Note Types and restart Anki to fix this problem."
                " Otherwise, please add the field back to the note type. "
                .format(field=str(e), name=lpcg_models.NAME))
            return

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
