# Before starting this code you need to install a MIDI player and set it to an environment.
# I used timidity, but you can use something else.
"""Install Timidity:

1: In console put in sudo apt-get install timidity
2: Set environment to timidity (typically /usr/bin/timidity)

Set your environment here: """
environment.set('midiPath', '/usr/bin/timidity')

#Imports music21. User guide to music21: https://web.mit.edu/music21/doc/usersGuide/

import music21
from music21 import *


def playnote():
    oknotes = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'c5']
    n = input("Press which note you would like to play! For high C, input C5.")
    sf = input("Is the note sharp or flat? Input s for sharp, f for flat, or nothing for neither.")
    if sf == 's':
        n = n + '#'
    if sf == 'f':
        n = n + "-"
    if n.lower() in oknotes:
        n = note.Note(str(n.upper()))
        n.duration.type = 'whole'
        return n.show('midi')
    else:
        return "Error: Out of Range. Please input a letter between A and G, or C5."


playnote()


n = 'd'
n = 'd' + '-'