*Warning. This README is incomplete and not 100% correct. However, it is so much
better than the README that I previously had posted here that I decided to
update with this one anyway.  Hopefully I will have a complete version finished
soon, as most of the part I have done is correct.*

Anki Lyrics/Poetry Cloze Generator (LPCG) is a Python script to ease the
creation of Anki cards for memorizing a long passage of text verbatim, such as
poetry or song lyrics.

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
after studying this way--that isn't the point. However, you will know the
entirety of the text, and if you run through it a couple of times and correct
yourself on any weak points, you probably will be able to do it the next time.
And better yet, you will continue to remember it on at least this level even if
you never see or hear of the song or poem outside of Anki for 25 years, enough
that even if you've lost your fluency you'll be able to pick it up again
quickly.

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
UTF-8. LPCG is *not* written to process text in Unicode at the moment, so if
you need non-Latin characters you may be in trouble. If you need this, please
contact me and I'll see what I can do about adding it.

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

Mac OS X and nearly all Linux distributions come with Python preinstalled. If
you want to check to be sure, open a terminal (Applications -> Utilities ->
Terminal on a Mac) and type "python". If you get a version number and a >>>
prompt, you're good. If it's not there for some reason, install it through your
distribution's package manager or Google for instructions if necessary.

On Windows, you can check if you have Python by attempting to start LPCG by
double-clicking on it.  If Windows tells you it doesn't recognize the file type,
you need to install Python. You can download Python from
<http://python.org/download/releases/2.7.3/>. If you know you have a 64-bit
operating system, download the Windows X86-64 MSI installer; otherwise, download
the Windows x86 MSI installer. Installation is straightforward and works just
like installing any other program.

Once you've gotten Python installed (if necessary), you're ready to run LPCG:
just double-click on lpcg.py to get started. No installation of LPCG itself is
required, so simply put the file in a convenient place to run when desired.

Running the Script
==================

When you run LPCG, you will be shown a copyright notice and a brief help screen.
Here's what information you need to give it:

1. *Input File.* Use your file manager (e.g., Windows Explorer, Finder) to
   locate a file of lyrics or poetry formatted for LPCG (see the section
   Generating Input Files). Drag and drop the file onto the LPCG terminal
   window; the path to the file should appear. Press _Enter_.
2. *Title.* Enter the title of the song here and press _Enter_. The title will
   be used to provide context when you're asked for the first line of the song
   or poem (otherwise, the question for the first line of a text would be
   indistinguishable from any others you studied).
3. *Tags.* If you want to add tags to all of the cards you're about to import,
   type them and press Enter. (Remember that tags are separated by spaces in
   Anki and cannot themselves contain spaces.) I like to add the title separated
   by underscores or in CamelCase (e.g., "the\_tyger" or "TheTyger") so that I
   can easily search for all the cards of a given song later on.

After entering this information, LPCG should generate the cards, write them to a
temporary file, and pull up Anki's import screen. Proceed to the next section.

Importing into Anki
===================

Studying
========


This is not a readme, this is scraps that might be useful for writing a readme. I'll get to it sometime.

Forum stuff about this script:
https://mail.google.com/mail/u/0/#search/lyrics/13a0572d7037e3fb:
You can't put review cards in order in Anki, as this is somewhat against the whole idea of spaced repetition. It would also pose some implementation difficulties in being able to show cards at the right time and stuff, which I won't get into unless you really want to know why.

But it is quite possible to memorize a text with discrete unordered cards; you just have to do it the right way. Here is what I do for song lyrics, which are similar:
First, I go through the song. I know most of the songs I try to memorize quite well by the time I begin, but I find a recording and listen to it (and usually sing along) a couple of times. With poetry, you should read through it; it would probably help to read out loud if you can.

Then I go to Anki and create cards with two lines of context and one clozed line:

CARD 1:
Q:
This is the first line
And this is the second line
[...]
A: This is the third line

CARD 2:
Q: 
And this is the second line.
This is the third line.
[...]
A: This is the fourth line.

I have a Bash script that automates the procedure of creating these cards from a text file of lyrics; let me know if you're interested in it.

Once I've learned all those cards, I find I can usually sing the song from memory, without ever having gone through the entire thing at all (except in my initial lookover). After you've had all the cards introduced for a couple of days, try to recite your poem: you'll probably be surprised with how well you know it. If you're still having trouble, take a look at the whole thing again on a piece of paper and try to sequence what you're still missing, and study for a couple more days.

If you find you don't know it well enough or are still struggling with putting things in order (which I find is rare, with two lines of context), you can create cards for each stanza and even a card for the entire thing, to make sure you can recite it that way as well. But don't do this until you have learned the three-line groupings.

Note that, while reviewing, I always sing the entire context (out loud, if I'm alone) before attempting to recall the clozed line; I find this helps with being able to remember what comes next in time later on. (Okay, I lied, I skip this step if I know the entire clozed line off the top of my head in less than a second or so, as that clearly means I know it well enough.)

Let me know if I could explain anything clearer. This is mostly my own method, but the idea of splitting things up and using overlapping clozes is a basic SRS idea.

Given the interest in this, I plan to improve my system a little bit and post some details on my website.

For now, I have attached a copy of the script and a one-card apkg with the note type, which implements a cloze deletion style while allowing the clozed line to be stored in a separate field and sorted by. I don't think it's strictly necessary—I probably could've handled it fairly well with the default cloze type—but it made more sense when I created it, so that's what I'm using now.

Instructions for use:
1) Set the script as executable.
2) Edit the script and set the first two variables to match your setup (Anki location and output file location).
3) Create a text file that contains your lyrics. The file should not have any blank lines; to indicate the end of a stanza, I use the marker (E) at the end of the final line. While the script can handle the spaces fine, it looks much nicer to have the (E)'s instead of blank lines and only one line of context once you get the data into Anki.
4) Run ./songcloze.sh <name_of_file>. If you want to specify an output location, you can add that as a second argument; otherwise the script uses the output directory you set plus input_file.tsv.
5) The script will run Anki (if not already running) and import the file. Select the Lyrics note type and click Import.

Currently there is no support for tagging cards, so you should do that manually after each import if you wish to (or sort by creation date later on to get them in order). I plan to include that feature later.

If you're using Windows, you can probably run this via a program called "Cygwin."

Instructions for use:
1) Set the script as executable.

I haven't done this on a Mac in a while, but I think you do this in the properties menu from right/control-clicking on it. IIRC, on a Mac you should also rename the file to "songcloze.command", though I'm not sure it matters when you're running in the terminal.
 
2) Edit the script and set the first two variables to match your setup (Anki location and output file location).

If you open it in a text editor, you'll see the following:
#!/bin/bash
# Song Cloze Generator
# by Soren Bjornstad
# Contact: soren.bjornstad@gmail.com
# http://www.thetechnicalgeekery.com/anki

# Set this to the location of Anki's executable, if not on the path.
ankipath="/home/soren/code/anki/anki-2.0-alpha2/ankiqt/anki"

# Set this to a folder where you want the completed tab-separated data files
# to be stored. Do not include trailing slash.
output_location="/home/soren/Anki/songs/Output"

Set the first variable (ankipath) to wherever Anki is located. You can probably just set this to "anki" (with the quotes). So it would say
     ankipath="anki"

Set the second to a path where you'd like to store the output files. If you like, you can actually just set this to "" to store the files to be imported into Anki in the same folder as whereever you run the script from. So:
     ankipath=""

Otherwise you can find the path of any folder on your system and put that in the quotes. On Windows and Linux you can find the path somewhere in the file browser; I assume Finder has a similar option.

4) Run ./songcloze.sh <name_of_file>. If you want to specify an output location, you can add that as a second argument; otherwise the script uses the output directory you set plus input_file.tsv.

Open up a terminal (I think it's in Applications → Utilities), use "cd" to change to the folder where you've put the script (you can use "ls" if you don't know the names of the folders where you currently are), and run the command
    ./songcloze.sh test_file
...assuming that the file you want to convert is called test_file.


Let me know if anything doesn't work.





--Tentative Windows instructions-- (private email)
1) Install Python 2.7 from http://python.org (direct link to the installer if you prefer: http://python.org/ftp/python/2.7.3/python-2.7.3.msi).
2) Import the attached apkg; it contains a note type needed for the script to work.
3) Create a text file that contains your lyrics using a program like Notepad. I listed formatting instructions on the original post.
4) Double-click on the Python script to run it; it'll prompt you for an input file. You can drag and drop the file onto the command prompt window to paste the path.
5) Press Enter and give an output file. If you're not familiar with pathnames, an easy way is to drag and drop a folder onto the window, then backspace the quotation mark and type \filename" (including the closing quote). This will place the file filename in the folder you dragged and dropped.
6) In Anki, choose File -> Import, select the output file, and select the note type that was provided in that apkg file (it's called "Lyrics" if I remember right). Import and your cards should be created.

Please let me know if anything doesn't work right, as I have not tried this script on Windows before.

