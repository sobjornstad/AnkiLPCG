import codecs

# pylint: disable=no-name-in-module
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

import aqt
from aqt.qt import QAction  # type: ignore
from aqt.utils import getFile, showWarning, askUser, tooltip
from anki.notes import Note

from . import import_dialog as lpcg_form
from .gen_notes import add_notes, cleanse_text
from . import models


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
        self.form.helpButton.clicked.connect(self.onHelp)

        self.addonConfig = self.mw.addonManager.getConfig(__name__)
        self.form.contextLinesSpin.setValue(self.addonConfig['defaultLinesOfContext'])
        self.form.reciteLinesSpin.setValue(self.addonConfig['defaultLinesToRecite'])
        self.form.groupLinesSpin.setValue(self.addonConfig['defaultLinesInGroupsOf'])

    def accept(self):
        "On close, create notes from the contents of the poem editor."
        title = self.form.titleBox.text().strip()

        if not title:
            showWarning("You must enter a title for this poem.")
            return
        escaped_title = title.replace('"', '\\"')
        if self.mw.col.find_notes(f'"note:{models.LpcgOne.name}" '  # pylint: disable=no-member
                                  f'"Title:{escaped_title}"'):
            showWarning("You already have a poem by that title in your "
                        "database. Please check to see if you've already "
                        "added it, or use a different name.")
            return
        if not self.form.textBox.toPlainText().strip():
            showWarning("There's nothing to generate cards from! "
                        "Please type a poem in the box, or use the "
                        '"Open File" button to import a text file.')
            return

        author = self.form.authorBox.text().strip()
        tags = self.mw.col.tags.split(self.form.tagsBox.text())
        text = cleanse_text(self.form.textBox.toPlainText().strip(), self.addonConfig)
        context_lines = self.form.contextLinesSpin.value()
        recite_lines = self.form.reciteLinesSpin.value()
        group_lines = self.form.groupLinesSpin.value()
        did = self.deckChooser.selectedId()

        try:
            notes_generated = add_notes(self.mw.col, Note, title, author, tags, text, did,
                                        context_lines, group_lines, recite_lines)
        except KeyError as e:
            showWarning(
                "The field {field} was not found on the {name} note type"
                " in your collection. If you don't have any LPCG notes"
                " yet, you can delete the note type in Tools -> Manage"
                " Note Types and restart Anki to fix this problem."
                " Otherwise, please add the field back to the note type. "
                .format(field=str(e), name=models.LpcgOne.name))  # pylint: disable=no-member
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

    def onHelp(self):
        """
        Open the documentation on importing files in a browser.
        """
        doc_url = "https://ankilpcg.readthedocs.io/en/latest/importing.html"
        QDesktopServices.openUrl(QUrl(doc_url))
