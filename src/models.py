"""
trmodels.py - self-constructing definitions of Anki models (note types)

Creating a note type in Anki is a procedural operation, which is inconvenient
and difficult to read when note types need to be defined in source code
rather than through the GUI. This module allows note types to be defined
declaratively.

It first defines TemplateData and ModelData classes which contain the logic
for creating templates and note types, then subclasses which define the
options and templates for each note type our application needs to create and
manage. A framework for checking if note types exist and have the expected
fields, and for changing between note types defined here, is also provided.

These classes are a bit unusual in that they are never instantiated and have
no instance methods or variables. The class structure is just used as a
convenient way to inherit construction logic and fields and group related
information together.

This mini-framework was originally created for TiddlyRemember and is
presented in slightly altered form here. The third project should combine the
two versions and create a standardized system!
"""
from abc import ABC
import inspect
import re
from textwrap import dedent
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Type
import sys

import aqt
from aqt.utils import askUser, showInfo
from anki.consts import MODEL_CLOZE
from anki.models import TemplateDict as AnkiTemplate
from anki.models import NotetypeDict as AnkiModel


class TemplateData(ABC):
    """
    Self-constructing definition for templates.
    """
    name: str
    front: str
    back: str

    @classmethod
    def to_template(cls) -> AnkiTemplate:
        "Create and return an Anki template object for this model definition."
        assert aqt.mw is not None, "Tried to use models before Anki is initialized!"
        mm = aqt.mw.col.models
        t = mm.new(cls.name)
        t['qfmt'] = dedent(cls.front).strip()
        t['afmt'] = dedent(cls.back).strip()
        return t


class ModelData(ABC):
    """
    Self-constructing definition for models.
    """
    name: str
    fields: Tuple[str, ...]
    templates: Tuple[Type[TemplateData]]
    styling: str
    sort_field: str
    is_cloze: bool
    version: str
    upgrades: Tuple[Tuple[str, str, Callable[[AnkiModel], None]], ...]

    @classmethod
    def to_model(cls) -> Tuple[AnkiModel, str]:
        """
        Create and return a pair of (Anki model object, version spec)
        for this model definition.
        """
        assert aqt.mw is not None, "Tried to use models before Anki is initialized!"
        mm = aqt.mw.col.models
        model = mm.new(cls.name)
        for i in cls.fields:
            field = mm.new_field(i)
            mm.add_field(model, field)
        for template in cls.templates:
            t = template.to_template()
            mm.addTemplate(model, t)
        model['css'] = dedent(cls.styling).strip()
        model['sortf'] = cls.fields.index(cls.sort_field)
        if cls.is_cloze:
            model['type'] = MODEL_CLOZE
        return model, cls.version

    @classmethod
    def upgrade_from(cls, current_version: str) -> str:
        """
        Given that the model is at version current_version (typically stored
        in the add-on config), run all functions possible in the updates tuple
        of the model. The updates tuple must be presented in chronological order;
        each element is itself a 3-element tuple:

        [0] Version number to upgrade from
        [1] Version number to upgrade to
        [2] Function taking one argument, the model, and mutating it as required;
            raises an exception if update failed.

        Returns the new version the model is at.
        """
        assert aqt.mw is not None, "Tried to use models before Anki is initialized!"
        model = aqt.mw.col.models.by_name(cls.name)

        at_version = current_version
        for cur_ver, new_ver, func in cls.upgrades:
            if at_version == cur_ver:
                func(model)
                at_version = new_ver
        if at_version != current_version:
            aqt.mw.col.models.save(model)
        return at_version

    @classmethod
    def in_collection(cls) -> bool:
        """
        Determine if a model by this name exists already in the current
        Anki collection.
        """
        assert aqt.mw is not None, "Tried to use models before Anki is initialized!"
        mm = aqt.mw.col.models
        model = mm.by_name(cls.name)
        return model is not None

    @classmethod
    def can_upgrade(cls, current_version: str) -> bool:
        """
        Return True if we know of a newer version of the model than supplied.
        """
        if cls.is_at_version(current_version):
            return False
        for cur_ver, _, __ in cls.upgrades:
            if current_version == cur_ver:
                return True
        return False

    @classmethod
    def is_at_version(cls, current_version: str) -> bool:
        "Return True if this model is at the version current_version."
        return current_version == cls.version


def upgrade_none_to_onethreeoh(mod):
    "Upgrade LPCG model from unversioned to version 1.3.0."
    mm = aqt.mw.col.models
    field = mm.new_field("Prompt")
    mm.add_field(mod, field)

    if '.nightMode .cloze' not in mod['css']:
        mod['css'] += "\n\n"
        mod['css'] += dedent("""
            .nightMode .cloze {
                filter: invert(85%);
            }
            """).strip()
    mod['css'] = mod['css'].replace('margin-left: -30px;', '')

    assert len(mod['tmpls']) == 1, "LPCG note type has extra templates!"
    mod['tmpls'][0]['qfmt'] = mod['tmpls'][0]['qfmt'].replace(
        '<span class="cloze">[...]</span>',
        dedent('''
            <div class="cloze">
                {{#Prompt}}{{Prompt}}{{/Prompt}}
                {{^Prompt}}[...]{{/Prompt}}
            </div>
        ''').strip()
    )
    mod['tmpls'][0]['afmt'] = mod['tmpls'][0]['afmt'].replace(
        '<span class="cloze">{{Line}}</span>',
        '<div class="cloze">{{Line}}</div>'
    )


def upgrade_onethreeoh_to_onefouroh(mod):
    "Upgrade LPCG model from 1.3.0 to version 1.4.0."
    mm = aqt.mw.col.models
    mm.add_field(mod, mm.new_field("Author"))

    mod['css'] = mod['css'].replace('.title {', '.title, .author {')

    assert len(mod['tmpls']) == 1, "LPCG note type has extra templates!"
    for side in ['qfmt', 'afmt']:
        mod['tmpls'][0][side] = mod['tmpls'][0][side].replace(
            '<div class="title">{{Title}} {{Sequence}}</div>',
            dedent('''
                <div class="title">{{Title}} {{Sequence}}</div>
                {{#Author}}<div class="author">{{Author}}</div>{{/Author}}
            ''').strip()
        )


class LpcgOne(ModelData):
    class LpcgOneTemplate(TemplateData):
        name = "LPCG1"
        front = """
            <div class="title">{{Title}} {{Sequence}}</div>
            {{#Author}}<div class="author">{{Author}}</div>{{/Author}}

            <br>

            <div class="lines">
                {{Context}}
                <div class="cloze">
                    {{#Prompt}}{{Prompt}}{{/Prompt}}
                    {{^Prompt}}[...]{{/Prompt}}
                </div>
            </div>
        """
        back = """
            <div class="title">{{Title}} {{Sequence}}</div>
            {{#Author}}<div class="author">{{Author}}</div>{{/Author}}

            <br>

            <div class="lines">
                {{Context}}
                <div class="cloze">{{Line}}</div>
            </div>
        """

    name = "LPCG 1.0"
    fields = ("Line", "Context", "Title", "Author", "Sequence", "Prompt")
    templates = (LpcgOneTemplate,)
    styling = """
        .card {
            font-family: arial;
            font-size: 20px;
            color: black;
            background-color: white;
        }

        p {
            margin-top: 0px;
            margin-bottom: 0px;
        }

        .lines {
            text-align: left;
            margin-left: 30px;
            text-indent: -30px;
            margin-right: 30px;
        }

        .cloze {
            font-weight: bold;
            color: blue;
        }

        .nightMode .cloze {
            filter: invert(85%);
        }

        .title, .author {
            text-align: center;
            font-size: small;
        }

        .indent {
            margin-left: 60px;
        }
    """
    sort_field = "Sequence"
    is_cloze = False
    version = "1.4.0"
    upgrades = (
        ("none", "1.3.0", upgrade_none_to_onethreeoh),
        ("1.3.0", "1.4.0", upgrade_onethreeoh_to_onefouroh),
    )


def ensure_note_type() -> None:
    """
    Create or update the LPCG note type as needed.
    """
    assert aqt.mw is not None, "Tried to use models before Anki is initialized!"
    mod = LpcgOne

    if not mod.in_collection():
        model_data, new_version = mod.to_model()
        aqt.mw.col.models.add(model_data)
        aqt.mw.col.set_config('lpcg_model_version', new_version)
        return

    # "none": the "version number" pre-versioning
    current_version = aqt.mw.col.get_config('lpcg_model_version', default="none")
    if mod.can_upgrade(current_version):
        r = askUser("In order to import new notes in this version of LPCG, "
                    "your LPCG note type needs to be upgraded. "
                    "This may require a full sync of your collection upon completion. "
                    "Would you like to upgrade the note type now? "
                    "If you say no, you will be asked again next time you start Anki.")
        if r:
            new_version = mod.upgrade_from(current_version)
            aqt.mw.col.set_config('lpcg_model_version', new_version)
            showInfo("Your LPCG note type was upgraded successfully. "
                    "Please take a moment to ensure your LPCG cards "
                    "are still displaying as expected so you can restore from a backup "
                    "in the event something is not working correctly.")
        return

    assert mod.is_at_version(aqt.mw.col.get_config('lpcg_model_version')), \
        "Your LPCG model is out of date, but I couldn't find a valid upgrade path. " \
        "You are likely to encounter issues. " \
        "Please contact the developer for assistance resolving this problem."
