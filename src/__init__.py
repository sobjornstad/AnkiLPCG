"""
LPCG - Lyrics/Poetry Cloze Generator
version 1.2.1
Copyright (c) 2016-2019 Soren Bjornstad <contact@sorenbjornstad.com>
License: GNU AGPL, version 3 or later: <http://www.gnu.org/licenses/agpl.html>
"""

import sys

# don't try to set up the UI if running unit tests
if 'pytest' not in sys.modules:
    # pylint: disable=import-error, no-name-in-module
    # pylint: disable=invalid-name
    import aqt
    from aqt.qt import QAction  # type: ignore

    from . import model_data as lpcg_models
    from .lpcg_dialog import LPCGDialog


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

    if aqt.mw is not None:
        action = QAction(aqt.mw)
        action.setText("Import &Lyrics/Poetry")
        aqt.mw.form.menuTools.addAction(action)
        action.triggered.connect(open_dialog)

        aqt.gui_hooks.profile_did_open.append(ensure_note_type)
