=========
Changelog
=========

LPCG 1.4.0
==========

Released on November 15, 2020.

* Add an *Author* field to the note type,
  which can optionally be set when adding poems
  (thanks to @cashweaver).
  The author displays just underneath the title and index when reviewing,
  if present.
* The Add Notes access key has been changed from :kbd:`a` to :kbd:`d`
  to resolve a conflict with :guilabel:`Author`
  (all the letters in *Author* were already taken!).
* Allow quotation marks to be used in the title of a poem,
  now that Anki is able to escape quotation marks in searches.
* Make the default values of the import spinboxes configurable.
* Add screenshots to the README.


LPCG 1.3.0
==========

* Added options *Lines to Recite* and *Lines in Groups of*.
* Add a *Prompt* field to the note type.
  This was added to support showing the user
  how many lines they're being asked to recite,
  but could be used for other things in the future.
  Backwards compatibility with existing notes is maintained
  by displaying ``[...]`` if the field is empty.
* The *Line* field now wraps each (or the only) line in ``<p>`` tags,
  to support multiple-line recitation with correct indentation.
  Existing LPCG notes without ``<p>`` tags will still display fine as well.
* Invert color of cloze deletions in night mode,
  as the default color is unnecessarily difficult to read on many screens.
* Added some automated regression testing.
* Add a *Help* button to the import dialog leading to the documentation.
* Under-the-hood refactorings and updates to newer features offered by Anki.
* Refresh the documentation and move to Read the Docs
  for a nice multi-page view instead of relying on GitHub's Markdown rendering.


LPCG 1.2.1
==========

* Provide a useful error message when generating notes
  and the LPCG note type is missing a required field.


LPCG 1.2.0
==========

* Support for Anki 2.1 (only).
* Fixed several minor bugs in splitting poems into stanzas
  that could result in end-of-stanza and end-of-poem markers
  appearing on lines by themselves.
* Fixed text flowing off the right side of mobile device screens
  (thanks to Jonta).


LPCG 1.1.0
==========

* Added support for changing the number of lines of context you want to see
  for a given poem.
  The default remains 2.

This is the last version that supports Anki 2.0.


LPCG 1.0.0
==========

LPCG was completely rewritten
and became a proper Anki add-on instead of a stand-alone Python script.
A new note type is also used with this version.


LPCG 0.9.4
==========

* Improve the user experience when the temporary folder is not writable
  or the user specifies a nonexistent file.
* Add a message explaining that Anki should have opened to import notes,
  in case it doesn't and the user is left sitting there wondering
  what's supposed to happen next.


LPCG 0.9.3
==========

* Fix typo in code that caused LPCG not to import successfully at all.


LPCG 0.9.2
==========

* Fix off-by-one error sometimes resulting in incorrect card generation.
* Allow dragging and dropping files onto the terminal window to work correctly
  in more situations.


LPCG 0.9.1
==========

* Tags should not be mandatory.


LPCG 0.9.0
==========

* First public release.
