Anki **Lyrics/Poetry Cloze Generator** (LPCG) is an add-on for
[Anki](http://ankisrs.net) to make it easier to study long passages of verbatim
text, like poetry or song lyrics.

<img style="float: right;" width=400px border="1" src=screenshots/studying.png>

This is LPCG 1.2.1. Versions in the 0.x series were standalone Python scripts
that had to be installed and run separately from Anki; the add-on approach
taken by 1.0 and above should be much easier to set up and use for most users.
Version 1.2.0 and above support Anki 2.1 only; 2.0 is no longer supported.

<img style="float: right;" height=300px border="1" src=screenshots/iphone.png>

Contents
========

* <a href="#Support">Support</a>
* <a href="#Theory">Theory</a>
* <a href="#Installation">Installation</a>
* <a href="#Use">Use</a>
* <a href="#Editing_LPCG_notes">Editing LPCG notes</a>
* <a href="#Summary_of_the_LPCG_note_type">Summary of the LPCG note type</a>
* <a href="#Customization">Customization</a>
* <a href="#Appendix_Initial_memorization">Appendix: Initial memorization of
  poetry</a>

<a id="Support">

Support
=======

If you have any questions which are not answered by this manual, you can email
me at anki@sorenbjornstad.com.

If you have found a bug or wish to suggest an improvement, you can post on the
issue tracker or submit a pull request [at
GitHub](https://github.com/sobjornstad/AnkiLPCG).


<a id="Theory">

Theory
======

(For clarity, in the remainder of this documentation, I’ll discuss “poetry,” but everything applies equally to songs, speeches, or whatever.)

Memorizing poetry can be a tough problem for Anki users: it isn’t obvious how
to divide it into discrete cards. People often try one of the following
approaches:

* Putting the whole poem onto one card. This is a bad idea because if you have
  trouble with any part of the poem, you’ll have to fail the entire card, and
  you will review far more often than you need to.
* Creating one card per line and defining an order for the cards, so Anki asks
  for the lines in order. Aside from this being impossible in the current
  version of Anki, spaced repetition scheduling doesn’t work properly unless
  the cards are in random order.

LPCG takes a different approach: it generates cards that can stand on their own
and make perfect sense in random order. Each card shows two lines from the poem
and then asks you to recite the third line following them. One card is created
per line, so that each line is tested exactly once.

In my experience, this is not a good way to *memorize* poetry: not seeing the
full context makes initial acquisition quite frustrating. However, it is a good
way to *review* poetry. This is fine, because as most Anki users know, the big
problem isn’t learning things in the first place, it’s remembering them for
long periods of time.

If you don’t know a good way of initially learning poems, look at the <a
href="#Appendix_Initial_memorization">Initial memorization</a> section at the
end of this manual.


<a id="Installation">

Installation
============

LPCG can be installed from [its AnkiWeb
page](https://ankiweb.net/shared/info/2084557901). The source is available [at
GitHub](https://github.com/sobjornstad/AnkiLPCG). LPCG, like Anki, is licensed
under the [GNU AGPL3](http://www.gnu.org/licenses/agpl.html).


<a id="Use">

Use
===

To add a poem to your collection, choose **Tools → Import Lyrics/Poetry**. You
will see the following window:

![The import dialog](screenshots/importing.png)

The options should be fairly self-explanatory. Note that the **Title** field
will be used to warn you if you already have this poem in your collection, as
well as appearing at the top of each of your cards.

The large text box, called the *poem editor*, contains the text from which your
cards will be generated. You can either type or paste a poem directly into the
editor or open a plain text file somewhere on your computer using the **Open
file** button. Lines beginning with the comment character `#` are ignored;
everything else in the editor will be treated as the text of your poem.

LPCG understands blank lines between stanzas as stanza breaks. The ends of
stanzas will be marked with the character **⊗** (this is a conventional marker
for end-of-stanza in some fields), and the very end of the poem will be marked
with the character **□**.

You can include one level of indentation by placing any number of spaces or
tabs at the beginning of the indented line(s). The LPCG note type also applies
a hanging indent to any lines that do not fit on the screen in their entirety.

Here is an example of a correctly formatted poem:

    # from “Little Gidding,” movement II
    # by T.S. Eliot

    Ash on an old man’s sleeve
    Is all the ash the burnt roses leave.
    Dust in the air suspended
    Marks the place where a story ended.
    Dust inbreathed was a house –
    The wall, the wainscot and the mouse.
    The death of hope and despair,
        This is the death of air.

    There are flood and drouth
    Over the eyes and in the mouth,
    Dead water and dead sand
    Contending for the upper hand.
    The parched eviscerate soil
    Gapes at the vanity of toil,
    Laughs without mirth.
        This is the death of earth.

When you’re done, click **Add notes** to add the poem to your collection.


<a id="Editing_LPCG_notes">

Editing LPCG notes
==================

Sooner or later you will probably find that you made a typo in one of your
poems. To correct the typo properly, you should *search for the typo in the
browser*, rather than just pressing edit, since it will be on three different
notes. Two of the errors will be in the *Context* field and one will be in the
*Line* field.


<a id="Summary_of_the_LPCG_note_type">

Summary of the LPCG note type
=============================

The four fields of the note type are as follows:

* **Line**: Contains the line this card asks you to recite.
* **Context**: Contains the two lines prior to *Line*. Note that this looks
  kind of oddly spaced in the editor (but normal in review) because the editor
  doesn’t use the same styling as the review window.
* **Title**: The title of the poem that this line comes from.
* **Sequence**: The line number (counting only text lines, not comments or
  blank lines) of *Line* in the original poem.

Note that LPCG takes the approach of creating a series of unrelated notes
rather than a single note. Creating one note per poem would have a number of
serious disadvantages:

* Sibling burying would get in the way – it can of course be turned off, but
  this would be confusing to some users.
* The amount of template boilerplate required would be absurd, and extremely
  large templates can cause syncing and other issues.
* LPCG would not be able to support poems of arbitrary length, since note types
  cannot contain an arbitrary number of fields or card types; at some point you
  would have to create multiple notes for the same poem, which would break the
  neat correspondence anyway.

The Sequence field helps to mitigate the disadvantages of having separate notes
– by searching for a given poem (e.g., `"note:LPCG 1.0" "Title:My Poem"`) and
then sorting by the Sequence field, you can still see and select the whole poem
at once.


<a id="Customization">

Customization
=============

If you’d like to customize the width of indents, you can make some changes in the styling section of the card types dialog:

* **Hanging indent** (when a line is too long for the screen): Change
  `margin-left` and `text-indent` in the `.lines` class. They should be
  inverses of each other (e.g., if `text-indent` is 30 pixels, `margin-left`
  should be -30 pixels). You’ll also need to change `margin-left` in the
  `.cloze` section to match `text-indent`.
* **Manual indent** (when an indent is given in the original poem text): Change
  `margin-left` in the `.indent` class.

The end-of-stanza and end-of-poem markers can be changed in the add-on config
(choose **Tools → Add-ons**, select LPCG in the list on the left, and click the
**Config** button).

<a id="Appendix_Initial_memorization">

Appendix: Initial memorization
==============================

The LPCG method requires you to memorize your poems before you start reviewing
them in Anki. As alluded to in the <a href="#Theory">Theory</a> section, there
are a lot of good ways to memorize poetry initially; it’s retaining it that’s
hard. If you already know how to memorize poetry, don’t listen to me, just use
your own method. But if you don’t have a good method, here’s one that works
well for me.

1. If you haven’t already, read through the poem carefully so you have a
   general idea of how it goes.
2. Read through the poem again, line by line. This time, immediately after you
   read each line, look away from the page and repeat the line back. If you
   stumble or get it wrong, try again until you get it right: read the line
   again, then look away and repeat it again. It is helpful but not strictly
   necessary to speak out loud.
3. Repeat step 2, but take two lines at a time – then repeat with three, four,
   five, and six. You will find it gets a little bit harder each time, but not
   much, since you’re getting more familiar with the poem as well; before you
   know it you’ll be able to remember six lines at a time. It is unnecessary to
   continue this process beyond six lines.
4. Set the poem aside until the next day – it is truly remarkable how much
   easier it is to continue after a good night’s sleep. Do not skip this step!
   The rest will be easy if you do it and quite frustrating if you don’t.
5. Try reciting the poem straight through. If the text is easy, you may have it
   already; otherwise, go back and work on any spots you don’t have down yet.
   No particular method is necessary at this point. Don’t work for more than a
   few minutes; just touching all the difficult spots is enough.
6. The next day, repeat step 5. Most likely the poem will now come very
   naturally to you. Particularly difficult texts may require one more day.

Once you have the poem learned, don’t forget to put it into Anki if you want to
remember it beyond the next couple of weeks – this is when LPCG comes into
play.

It is totally fine to take breaks during step 3, even doing it over several
days; you’ll spend 90% of your concentrated time in this step, and it’s not
helpful to try to work when you’re tired.
