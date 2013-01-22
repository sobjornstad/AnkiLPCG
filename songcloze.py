#!/usr/bin/env python
# Song Cloze Generator
# by Soren Bjornstad
# Contact: soren.bjornstad@gmail.com
# http://www.thetechnicalgeekery.com/anki

ankipath = "/home/soren/code/anki/unstable/ankiqt/anki"
default_input = ''
default_output = ''
default_title = ''
tag_separator = ''

from sys import argv
from subprocess import call

def print_help():
    print "    Lyrics/Poetry Cloze Generator"
    print "    Copyright 2013 Soren Bjornstad; see LICENSE for details.\n"
    print "    Input File: Drag and drop the input file you wish to use " \
              "onto this window."
    print "    Title:      This will be used to prompt you for the first line " \
              "of the text."
    print "    Tags:       This will be fed to Anki as the Tags field of each " \
              "card."
    print "\n    For further help, see the README file.\n"

def get_data(msg):
    data = ''
    while not data:
        data = raw_input("%s: " %msg)

    return data

def next_line(file):
    return (file.readline().rstrip())

def open_anki(output_file):
    call([ankipath, output_file])

def main():
    print_help()

    # Ask user for file and song names.
    input_file = get_data("Input File")
    title = get_data("Title")
    tag = get_data("Tags")

    # Open input and output files.
    lyrics_file = open(input_file)
    anki_file = open(output_file, 'w')

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

    line1 = "[First Line] (%s)\t%s\n" % (song_title, lyrics_first_line)
    line2 = "[Beginning]<br>%s\t%s\n" % (lyrics_first_line, lyrics_second_line)
    cards_data += line1
    cards_data += line2

    # Set variables to be used in the loop.
    context1 = next_line(lyrics_file)
    context2 = next_line(lyrics_file)
    current_line = next_line(lyrics_file)

    # Loop through the remainder of the cards.
    i = 3 # We already did the first two cards
    while i <= total_lines:
        cards_data += "%s<br>%s\t%s\n" % (context1, context2, current_line)
        context1 = context2
        context2 = current_line
        current_line = next_line(lyrics_file)
        i += 1

    # Write cards and clean up.
    anki_file.write(cards_data)
    anki_file.close()
    lyrics_file.close()

    # Import file to Anki.
    open_anki()

main()
