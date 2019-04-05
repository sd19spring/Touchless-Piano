:Name: Touchless Piano - Interactive Visualization, Software Design
:Authors: Sparsh Bansal, Lee Smith
:Version: 2.0

The Touchless Piano is an Interactive Visualization project in Software Design at Olin College of Engineering.

Requirements
============

Interactive Visualization Version 2.0 requires the following Python packages

.. code-block:: python

    import cv2
    import numpy as np
    import music21
    import * from music21

A MIDI player is also required. All testing used the timidity MIDI player.

Installation
============

The easiest and fastest way to get the packages up and running:

.. code-block:: python

    sudo apt-get install python-opencv
    sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-noseimport requests

In order to install timidity, input the following on the command line:
    sudo apt-get install timidity

In order for the player to work, the envrionment must be set. The base location is included in the code. If your MIDI player is in a different location, it must be updated for this code to function.

Set location:
     environment.set('midiPath', '/path/location/')
Default location:
     'usr/bin/timidity' 
  
Documentation
=============

We have added comments for every line of code that we felt could be beneficial for someone to understand the program

Note: We haved added comments especially on the imported packages and code so that we can fully understand the code written by someone else. We have cited the sources wherever appropriate. 

More documentation can be found in the file documentation.txt

Contributing Works
==================

We used information from:

:i: Think Python - Allen Downey

:ii: SciPy.org

:iii: OpenCV

:iiii: User's Guide, music21 (MIT)

Source URLs:
======
Think Python:
https://www.greenteapress.com/thinkpython/thinkpython.pdf

Music21:
https://web.mit.edu/music21/doc/usersGuide/index.html
