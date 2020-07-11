===================================
Technical Details and Customization
===================================

Here's some technical and architectural mumbo-jumbo
that you probably don't need to use LPCG
but might be useful if you want to customize LPCG or are just curious.


The LPCG note type
==================

The note type has five fields:

Line
    Contains the line or lines this card asks you to recite.
    Since LPCG 1.3, each line is enclosed in a ``<p>`` tag.
    For backwards compatibility,
    the template is also required to correctly display this field
    if it contains a single line without any ``<p>`` tags.

    Both the *Line* and *Context* fields
    look kind of oddly spaced in the editor due to the use of ``<p>`` tags,
    because the editor doesn’t use the same styling as the review window
    and this can't easily be customized.

Context
    Contains the several lines prior to *Line*,
    to give you an idea of what to recite.
    
Title
    The title of the poem that this line comes from.

Sequence
    The line number (counting only text lines, not comments or blank lines)
    of the first line of the *Line* field in the original poem.

    If the *Lines in Groups of* :ref:`setting <Generation settings>`
    was set to a value greater than 1,
    the actual line number in the original poem is
    the sequence number multiplied by *Lines in Groups of*,
    minus *Lines in Groups of*, plus 1.

Prompt
    If this field is populated, it will appear instead of ``[...]``
    on the question side.
    
    *New in LPCG 1.3.*

It is safe to add additional fields to the note type
if you wish to include more metadata on your poems.
The only likely issue would be if LPCG added a new field in the future
and its name happened to conflict with yours;
even then, this wouldn't cause any data loss,
you'd just have to rename your own field if you wanted to continue using it.


Why separate notes?
===================

LPCG takes the approach of creating a series of unrelated notes,
rather than a single note.
Creating one note per poem would have a number of serious disadvantages:

* Sibling burying would get in the way – it can of course be turned off, but
  this would be confusing to some users.
* The amount of template boilerplate required would be absurd, and extremely
  large templates can cause syncing and other issues.
* LPCG would not be able to support poems of arbitrary length, since note types
  cannot contain an arbitrary number of fields or card types; at some point you
  would have to create multiple notes for the same poem, which would break the
  neat correspondence anyway.

The Sequence field helps to mitigate the disadvantages of having separate notes
– by searching for a given poem (e.g., ``"note:LPCG 1.0" "Title:My Poem"``)
and then sorting by the Sequence field,
you can still see and select the whole poem at once.

One possible area for future improvement
would be caching the poem or its parsed representation
so that a poem's notes could be edited from a poem-editor-like text box
after initial creation.
At the moment, this feels like gold-plating since poems rarely need editing
and I have not seen any demand for such a feature.


Customizing styling
===================

If you’d like to customize the width of indents, you can make some changes in the styling section of the card types dialog:

* **Hanging indent** (when a line is too long for the screen):
  Change ``margin-left`` and ``text-indent`` in the ``.lines`` class.
  They should be inverses of each other
  (e.g., if ``text-indent`` is 30 pixels, ``margin-left`` should be -30 pixels).
  You’ll also need to change ``margin-left`` in the ``.cloze`` section
  to match ``text-indent``.
* **Manual indent** (when an indent is given in the original poem text):
  Change ``margin-left`` in the ``.indent`` class.

The end-of-stanza and end-of-poem markers can be changed in the add-on config
(choose :menuselection:`Tools --> Add-ons`,
select LPCG in the list on the left,
and click the :guilabel:`Config` button).

As of version 1.3, LPCG inverts the color of cloze deletions in night mode,
as the default solid blue is quite difficult to read in night mode
on many screens.
If you don't like the color,
you can change it in the styling rule `.nightMode .cloze`.
If you want it back to how it was in LPCG 1.2,
just leave the `{braces}` empty instead of removing the rule --
if you remove the rule,
LPCG will assume you haven't gotten the update yet
and inject the code back into your template next time you start Anki.
