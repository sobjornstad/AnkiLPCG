Anki Lyrics/Poetry Cloze Generator (LPCG) is a Python script to ease the
creation of Anki cards for memorizing a long passage of text verbatim, such as
poetry or song lyrics.

For more information on Anki, see <http://ankisrs.net>.

License
=======

Copyright (c) 2013 Soren Bjornstad. Permission is granted to copy, distribute
and/or modify this document under the terms of the GNU Free Documentation
License, Version 1.3 or any later version published by the Free Software
Foundation; with no Invariant Sections, no Front-Cover Texts, and no Back-Cover
Texts.  A copy of the license can be found in the COPYING file or at
<http://www.gnu.org/copyleft/fdl.html>.

Support
=======

If you have any questions which are not answered by this manual, you may either
email me at anki@sorenbjornstad.com or post on the Anki help forum
(<https://groups.google.com/forum/?fromgroups=#!forum/ankisrs>). I read the
forum daily, as I am employed answering support questions for Anki proper
there.

If you have found a bug or wish to suggest an improvement, you may post on the
issue tracker or submit a pull request at GitHub:
<https://github.com/sobjornstad/AnkiLPCG>.

Theory
======

It is extremely difficult and very bad form to put an entire poem into Anki and
try to memorize it as a single card. What people often want to do is define an
order of the cards, so that Anki asks them for the lines in order. At first
glance this seems to make sense: when you want to recite a poem or sing a song,
you go through it in order, right? But spaced repetition and Anki work well only
when the cards are placed in random order. Therefore, the trick is to provide
enough context that you can figure out what point in the text you are at on
every card.

I have found that two lines of context is enough to allow me to recall the
third line without being excessively long. When studying, I sing through the
first two lines of the lyrics, then try to answer the third. My goal is to go
for fluency so I don't have to stop and think, like I would if I were singing
it.

You probably won't be able to recite a poem or sing a song completely fluently
after studying this way. However, you should know the text quite well, and if
you run through it a couple of times and correct yourself on any weak points,
you probably will be able to do it the next time. And better yet, you will
continue to remember it on at least this level even if you never see or hear of
the song or poem outside of Anki for 25 years, enough that even if you've lost
your fluency you'll be able to pick it up again quickly.

LPCG allows you to easily generate overlapping cloze deletion cards with two
lines of context for the entire text of a song or poem. Read on to find out how.

Generating Input Files
======================

LPCG accepts simple text files as input. Each line of the song/poem should be
on a separate physical line of the text file, just as you would normally write
it. For instance:

    Tyger! Tyger! burning bright
    In the forests of the night,
    What immortal hand or eye
    Could frame thy fearful symmetry?

You should *not* use blank lines between stanzas, as this will cause a nasty
blank line to appear in your Anki cards (the cloze will contain nothing).
Instead, I like to put an (E) at the end of the final line of a stanza. This
way, the generated card will look something like this:

    What immortal hand or eye
    Could frame thy fearful symmetry? (E)
    [...]

This allows you to know that the next line is the start of the next stanza
while still looking good and not producing useless cards.

I haven't run into any encoding issues myself; I've saved my files in ASCII or
UTF-8. As a test, I tried putting some Japanese characters in a text file and
LPCG processed it correctly, so I think it should deal with any Unicode
characters properly. Please let me know if something doesn't work.

Installing the Note Type
========================

In order to use LPCG, you first need to add the LPCG note type to your
collection. LPCG ships with a file called "lpcg\_note\_type.apkg," which
contains one card of the LPCG note type. You can import this into Anki by
double-clicking on it; if it succeeds, one dummy card will be added to your
Default deck. After the import is successful, you may safely delete this test
card and the note type will remain.

Installing the Script
=====================

Mac OS X and nearly all Linux distributions come with Python preinstalled.

On Windows, you can check if you have Python by attempting to start LPCG by
double-clicking on it.  If Windows tells you it doesn't recognize the file type,
you need to install Python. You can download Python from
<http://python.org/download/releases/2.7.3/>. If you know you have a 64-bit
operating system, download the Windows X86-64 MSI installer; otherwise, download
the Windows x86 MSI installer. Installation is straightforward and works just
like installing any other program.

On Linux and Mac OS X, you may need to set the script as executable. (You'll
know this if you attempt to run it and nothing happens or a text editor opens
instead.) You can either do this through your file browser (details depend on
your computer), or universally by opening a terminal (Applications -> Utilities
-> Terminal on a Mac), typing *sudo chmod 755*, then a space, then dragging and
dropping the script onto the terminal window, and finally pressing Enter.

Setting a Custom Anki Location
==============================

LPCG assumes that your Anki executable is stored in one of these locations:
- 'C:\Program Files\Anki\anki.exe' (or Program Files (x86)) on Windows
- '/Applications/Anki.app/Contents/MacOS/Anki' on Mac OS X
- 'anki' (on the system path) on Linux

If it isn't, you'll receive a warning when you start LPCG telling you to define
a custom Anki location. You don't *have* to do this, but if you don't you'll
have to manually import a temporary file in an awkward location every time you
generate cards. Here's how to fix it:

1. Find a shortcut to Anki, open up the Properties for it, and determine the
   full path to the target. The specifics depend on your operating system. The
   path should be fairly long and contain slashes (/) or backslashes (\\).
2. Open the lpcg.py file in a text editor such as Notepad or TextEdit. You can
   either start the text editor first and use File -> Open to open the file or
   try right-clicking on the file and looking for an option such as "Edit" or
   "Open With."
3. Go to roughly line 25, inside the box made of hashes. You will see a line
   that looks like *custom\_anki\_location = ''*. Type or paste the path you got
   in step 1 between the single quotation marks.
4. If your path contains *backslashes*, \\, usually only if you're using
   Windows, change every backslash to two backslashes in a row (\\\\).
5. Save the file and restart LPCG. The warning message should be gone now.

If you believe that you installed Anki in a standard location and LPCG should
search that location by default, please contact me (see the Support section)
and provide the path and I will add it.

Running the Script
==================

On Windows, double-click on the file. On Linux, run './lpcg.py'. On Mac OS X, I
believe you can double-click as well, but I'm not certain.

When you run LPCG, you will be shown a copyright notice and a brief help screen.
Here's what information you need to give it:

1. *Input File.* Use your file manager (e.g., Windows Explorer, Finder) to
   locate a previously created file of lyrics or poetry formatted for LPCG (see
   the section Generating Input Files). Drag and drop the file onto the LPCG
   terminal window; the path to the file should appear. Press _Enter_.
2. *Title.* Enter the title of the song or poem here and press _Enter_. The
   title will be used to provide context when you're asked for the first line
   of the song or poem (otherwise, the question for the first line of a text
   would be indistinguishable from any others you studied).
3. *Tags.* If you want to add tags to all of the cards you're about to import,
   type them and press Enter. (Remember that tags are separated by spaces in
   Anki and cannot themselves contain spaces.) I like to add the title
   separated by underscores or in CamelCase (e.g., "the\_tyger" or "TheTyger")
   so that I can easily search for all the cards of a given song later on.

After entering this information, LPCG will generate the cards, write them to a
temporary file, and pull up Anki's import screen. Proceed to the next section.

Importing into Anki
===================

After running LPCG, Anki should come up and display the Import dialog. Going
from top to bottom:

- *Type*: Set the note type to LPCG.
- *Deck*: Set the deck to whatever deck you'd like to place the new cards in.
- *Fields separated by*: Tab should be selected automatically, but if it's not,
  do so.
- *Duplicate handling*: As long as you are pretty sure that no other song has
  the same two lines anywhere in the song (which is probably unlikely), select
  *Update existing notes when first field matches*.
- *Allow HTML in fields*: Make sure this is selected or the line breaks will
  not import correctly.
- *Field mapping*: Field 1 should be mapped to Context and field 2 to Line.

After checking that the settings are correct, click the *Import* button to the
right of the field mapping settings (not the *Close* button in the
lower-right). Anki should display "Importing complete" and a count of the
number of cards that were generated.

Updating LPCG Cards
===================

If you want to make changes to your cards later on (for instance, to correct a
typo or add some part of the song or poem that you forgot), the easiest way is
to change the original text file, then import it again, making sure to select
the "update" option in the import dialog box (see *Importing into Anki*, above).

Studying
========

Studying LPCG cards works just like studying normal cloze cards in Anki. (The
underlying mechanism is different; it does not use the actual cloze deletion
function, but unless you go into the template it looks the same.)

While studying, I find it helpful to say or sing the context out loud before
attempting to answer; this also helps you practice as if you were actually doing
it.

After studying for a week or two, try singing the song or reciting the poem:
you'll probably know it fairly well. If you would like to practice fluency, you
can copy and paste larger chunks such as whole stanzas into new Anki cards
manually, or even add a card that asks you to try saying/singing the whole
thing.
