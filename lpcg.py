#!/usr/bin/env python

# Anki Lyrics/Poetry Cloze Generator
# Copyright 2013 Soren Bjornstad.
# Version 0.9.1
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Contact Me:
# anki@sorenbjornstad.com
# http://www.thetechnicalgeekery.com/anki

###############################################################################
# If Anki is installed in a nonstandard location on your system, set this to
# the path to the executable that needs to be run to start Anki.

custom_anki_location = ''

###############################################################################

import tempfile
import os
import sys
from sys import argv
from subprocess import call

def print_help():
    print "    Lyrics/Poetry Cloze Generator v0.9.0"
    print "    Copyright 2013 Soren Bjornstad; see COPYING for details.\n"
    print "    Input File: Drag and drop the input file you wish to use " \
              "onto this window."
    print "    Title:      This will be used to prompt you for the first line " \
              "of the text."
    print "    Tags:       This will be fed to Anki as the Tags field of each " \
              "card."
    print "\n    For further help, see the README.\n"

def get_data(msg, required=True):
    data = ''
    while not data:
        data = raw_input("%s: " % msg)
        if not required:
            break

    return data.strip()

def next_line(file):
    return (file.readline().rstrip())

def locate_anki_executable():
    if custom_anki_location:
        if os.path.exists(custom_anki_location):
            return custom_anki_location
        else:
            print "*****\nError: Your custom Anki location does not exist! " \
                  "Please check the pathname and\n       try again.\n*****\n"
            return None

    if sys.platform.startswith('win32'):
        # based on whether we're using 32- or 64-bit Windows
        if 'PROGRAMFILES(X86)' in os.environ:
            anki_location = os.environ['PROGRAMFILES(X86)']
        else:
            anki_location = os.environ['PROGRAMFILES']

        anki_location = anki_location + '\Anki\\anki.exe'

    elif sys.platform.startswith('linux2'):
        anki_location = 'anki'

    elif sys.platform.startswith('darwin'):
        anki_location = '/Applications/Anki.app/Contents/MacOS/Anki'


    if os.path.exists(anki_location):
        return anki_location
    else:
        print "*****" \
              "\nWARNING: LPCG could not locate your Anki executable and " \
              "will not be able to\n         automatically import the " \
              "generated cloze deletions. To solve this\n         problem, " \
              "please see the \"Setting a Custom Anki Location\" section in " \
              "the\n         README." \
              "\n*****\n"
        return None


def open_anki(ankipath, anki_file):
    call([ankipath, anki_file.name])

def main():
    ankipath = locate_anki_executable()
    print_help()

    # Ask user for file and song names.
    input_file = get_data("Input File")
    title = get_data("Title")
    tags = get_data("Tags (optional)", required=False)

    # Open input and output files.
    lyrics_file = open(input_file)
    anki_file = tempfile.NamedTemporaryFile('w', delete=False)

    # Find total lines in file for the loop.
    total_lines = len(lyrics_file.readlines())
    lyrics_file.seek(0)

    # Data string to be added to.
    cards_data = ""

    # Make the first lines, as they're different from the rest (there aren't two
    # lines of context to use yet).
    lyrics_first_line = next_line(lyrics_file)
    lyrics_second_line = next_line(lyrics_file)
    lyrics_file.seek(0)

    line1 = "[First Line] (%s)\t%s\n" % (title, lyrics_first_line)
    line2 = "[Beginning]<br>%s\t%s\n" % (lyrics_first_line, lyrics_second_line)
    cards_data += line1
    cards_data += line2

    # Set variables to be used in the loop.
    context1 = next_line(lyrics_file)
    context2 = next_line(lyrics_file)
    current_line = next_line(lyrics_file)

    # Loop through the remainder of the cards.
    i = 3
    while i <= total_lines:
        cards_data += "%s<br>%s\t%s\n" % (context1, context2, current_line)
        context1 = context2
        context2 = current_line
        current_line = next_line(lyrics_file)
        i += 1

    # Write cards.
    anki_file.write("tags:%s\n" % tags)
    anki_file.write(cards_data)
    anki_file.close()
    lyrics_file.close()

    # Import file to Anki, if a location has been found.
    if ankipath:
        open_anki(ankipath, anki_file)
    else:
        print "\nDone! Now import the file %s into Anki. To avoid having to " \
              "do this manually in the future,\nconsider setting the path " \
              "to Anki in the script file, as described in the README." \
              % anki_file.name
        raw_input("== Press Enter to close the Generator. ==")

main()
