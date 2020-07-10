# -*- coding: utf-8 -*-

"""
Parameters and templates for the LPCG note type. See the create_note_type()
function in the main add-on file for implementation.

These are the note type definitions for LPCG 1.0.
"""

NAME = "LPCG 1.0"
FIELDS = ("Line", "Context", "Title", "Sequence")
TEMPLATE_NAME = "LPCG1"
SORT_FIELD = FIELDS.index("Sequence")

FRONT_TEMPLATE = """
<div class="title">{{Title}} {{Sequence}}</div>

<br>

<div class="lines">
{{Context}}
<span class="cloze">[...]</span>
</div>
""".strip()

BACK_TEMPLATE = """
<div class="title">{{Title}} {{Sequence}}</div>

<br>

<div class="lines">
{{Context}}
<span class="cloze">{{Line}}</span>
</div>
""".strip()

STYLING = """
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
 margin-left: -30px;
}

.nightMode .cloze {
 filter: invert(85%);
}

.title {
 text-align: center;
 font-size: small;
}

.indent {
 margin-left: 60px;
}
""".strip()


NIGHTMODE_CLOZE = """
.nightMode .cloze {
 filter: invert(85%);
}
""".strip()
