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

# Check for needed arguments.
if [ "$1" = "" ]; then
        echo "Usage: songcloze.sh <filename> [<outputfile>]"
        exit
fi

if [ "$2" = "" ]; then
        echo "Using $output_location/$1.tsv as output name."
        outputfile=$output_location/$1.tsv
else
        outputfile=$2
fi

read -p "Enter the title of this song (Return uses filename): " title
if [ "$title" = "" ]; then
        title=$1
fi

# Delete any previous output file. This is not strictly necessary, but looks cleaner.
touch $outputfile && rm $outputfile

# The first two lines are special; one has no context and the other has only
# one line. We're assuming the file has at least three lines.
echo -e "[First Line ($title)]\t$(head -n 1 $1)" > $outputfile
echo -e "[Beginning]<br>$(head -n 1 $1)\t$(head -n 2 $1 | tail -n 1)" >> $outputfile

# Initialize counters.
context1counter=1
context2counter=2
clozelinecounter=3
maxline=$( wc -l < $1 )

# Do the rest of the song.
while [ $clozelinecounter -le $maxline ]; do
        context1=$( head -n $context1counter $1 | tail -n 1 )
        context2=$( head -n $context2counter $1 | tail -n 1 )
        clozeline=$(head -n $clozelinecounter $1 | tail -n 1)

        echo -e "$context1<br>$context2\t$clozeline" >> $outputfile

        let context1counter=context1counter+1
        let context2counter=context2counter+1
        let clozelinecounter=clozelinecounter+1

done

# Import into Anki.
$ankipath $outputfile
