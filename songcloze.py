#!/usr/bin/env python
from sys import argv

# to clarify a few messy spots
def next_line(file):
    return (file.readline().rstrip())

def generate_tag(title):
    # Pattern for changing song titles to tags. If you prefer underscores
    # to CamelCase, you can use title.replace(' ', '_') instead here.
    return title.replace(' ', '')

# Ask user for file and song names.
input_file = raw_input("Lyrics (Input) File:")
output_file = raw_input("Cards (Output) File (Return for inputfile.tsv): ")
song_title = raw_input("Song Title: ")

# Remove spaces to generate tags.
tag = generate_tag(song_title)

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
