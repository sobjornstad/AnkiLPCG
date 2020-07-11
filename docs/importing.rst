===============
Importing Poems
===============

To add a poem to your collection,
choose :menuselection:`Tools --> Import Lyrics/Poetry`.
You will see the following window:

.. image:: screenshots/importing.*

Set the options and enter a poem as described below,
then click :guilabel:`Add notes`
to add notes for the new poem to your collection.


Basic options
=============

The **Title** of your poem will appear at the top of all your cards
so you know what you're reviewing.
It's also used to warn you
if you already have a poem by that title in your collection.

The **Tags** and **Deck**
will be attached to all notes generated from this poem
and work the same way as they do elsewhere in Anki.


The poem editor
===============

The large text box, called the *poem editor*,
contains the text from which your cards will be generated.
You can either type or paste a poem directly into the editor
or open a plain text file somewhere on your computer
using the **Open file** button.

The poem editor recognizes standard typographical conventions for poetry:

Stanza breaks
    Leaving a blank line
    (that is, a line containing no characters, or only whitespace)
    starts a new stanza.
    Blank lines at the start or end of the poem are ignored,
    and consecutive blank lines are treated as a single blank line.

    Stanza breaks don't appear as vertical space during reviews.
    Instead, the character **⊗** appears at the end of a line that ends a stanza,
    and the character **□** appears at the end of the poem's final line.

Indentation 
    Placing any number of spaces or tabs at the start of a line
    creates an indented line.
    Only one level of indentation is recognized,
    as poems that use more than one level of indentation are extremely rare,
    and this frees you from minutiae about how many spaces or tabs to use.

    LPCG also applies a hanging indent at review time
    to any lines that do not fit on your device's screen in their entirety.
    This hanging indent is twice the size of a "hard" indent
    that's part of the poem.

Comments
    Lines beginning with the comment character ``#`` are ignored,
    as is anything after the first ``#`` within a text line;
    everything else in the editor will be treated as the text of your poem.

    If you keep your poems in text files,
    you might want to use this to include annotations
    or information about the title or author.


Here is an example of a correctly formatted poem:
::

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


Generation settings
===================

The three numeric spin-boxes
allow you to customize how much text appears on each card.
Tweaking these settings is entirely optional;
the defaults are sufficient for most poems.

Lines of Context
    The number of lines that will be shown
    on the question side of each card as a prompt.
    With the default of 2, you'll see 2 lines of the poem
    and then be asked to recite the following line(s).
    
    At the very beginning of the poem,
    fewer lines of context will be available
    (e.g., there is no context at all for the first line
    save the title of the poem).
    If fewer lines of context are available than the value of this option,
    the text ``[Beginning]`` will appear on the question side of the card,
    followed by whatever context is available (if any).

Lines to Recite
    The number of lines that will be revealed
    on the answer side of each card.
    With the default of 1, a single line will be shown after the context lines.

    If *Lines to Recite* is more than 1,
    the cloze prompt ``[...]`` on the generated cards
    will show the number of lines that you need to recite,
    e.g., ``[...3]`` if there are three lines to recite.

    If the number of lines in your poem
    is not evenly divisible by *Lines to Recite*
    (e.g., you set it to 3 in a 16-line poem),
    one or more cards at the end will have fewer lines to recite;
    the cloze prompt will be adjusted accordingly.

    *New in LPCG 1.3.*

Lines in Groups of
    .. warning::
        This option can be confusing.
        If the two preceding options are enough to meet your needs,
        don't even bother reading this section!

    If this option is greater than 1,
    the physical lines in the poem editor will be grouped into "virtual lines"
    which will then be treated in accordance
    with the *Lines of Context* and *Lines to Recite* options.
    This can be useful if your poem has a large number of extremely short lines.

    For example, if you set *Lines in Groups of* to 2,
    *Lines of Context* to 2,
    and *Lines to Recite* to 1,
    you'll get cards that show 4 physical lines of context
    and ask you to recite 2 lines.

    At first glance, this may appear to be exactly the same thing as 
    doubling the values of *Lines of Context* and *Lines to Recite*.
    However, increasing those values
    merely increases the number of lines that appear on each card,
    keeping the number of cards and the amount of overlap the same,
    whereas grouping lines
    results in generating fewer cards that have less overlap.
    The best way to understand this is by example.
    Say we have the following uninspired poem:
    ::

        A
        B
        C
        D
        E
        F
        G
        H

    With the lines in groups of two using the settings described above,
    we would get the following cards:
    ::

        [Beginning] ==> A B
        [Beginning] A B ==> C D
        A B C D ==> E F
        ...et cetera

    If we instead were to set *Lines in Groups of* to 1,
    *Lines of Context* to 4,
    and *Lines to Recite* to 2,
    we would get:
    ::

        [Beginning] ==> A B
        [Beginning] A => B C
        [Beginning] A B => C D
        [Beginning] A B C => D E
        A B C D => E F
        B C D E => F G
        ...et cetera

    *New in LPCG 1.3.*


Editing LPCG notes
==================

Sooner or later you will probably find
that you made a typo in one of your poems.
To correct the typo completely,
you must *search for the typo in the browser*,
rather than just pressing edit,
since the typo will be included on several generated notes.
