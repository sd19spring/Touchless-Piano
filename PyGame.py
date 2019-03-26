#!/usr/bin/env python

"""
Mini Project 4 - Checkpoint 1
Author - Sparsh Bansal
Reference - https://github.com/Zulko/pianoputer

"""

# for reading and writing WAV files in the program
from scipy.io import wavfile

# for getting user-friendly comman-line interfaces
import argparse

import numpy as np
import pygame
import sys

# for issuing warnings to the user to alert them of some condition in the program
import warnings

def speedx(snd_array, factor):
    """
    Speeds up / slows down a sound, by some factor. 
    
    """
    # np.arrange gives us an array of evenly spaced values (space = factor) between 0 and the required length
    # np.round rounds the values of the array to integer values that can be used by the rest of the program
    indices = np.round(np.arange(0, len(snd_array), factor))
    # selection of indices based on indexing into the array of indices and comparing the values to the length of the input array
    # .astype(int) converts all the non-integer values in the array to integers 
    indices = indices[indices < len(snd_array)].astype(int)
    return snd_array[indices]

def stretch(snd_array, factor, window_size, h):
    """
    Stretches/shortens a sound, by some factor. 
    
    """

    # creates an array of zeroes of the size of 'window_size'
    phase = np.zeros(window_size)
    # creates a 'hanning window' of the size of the 'window_size', which is a window created using a weighted cosine
    hanning_window = np.hanning(window_size)
    # 
    result = np.zeros(int(len(snd_array) / factor + window_size))

    for i in np.arange(0, len(snd_array) - (window_size + h), h*factor):
        i = int(i)
        # Two potentially overlapping subarrays
        a1 = snd_array[i: i + window_size]
        a2 = snd_array[i + h: i + window_size + h]

        # The spectra of these arrays
        # fft computes the one-dimensional n-point discrete Fourier Transform of the scaled subarrays
        # This is required in order to obtain the specific frequencies that are making up the sound
        # as a function of time - which are required by the program for the output. 
        s1 = np.fft.fft(hanning_window * a1)
        s2 = np.fft.fft(hanning_window * a2)

        # Rephase all frequencies
        phase = (phase + np.angle(s2/s1)) % 2*np.pi

        a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
        i2 = int(i/factor)
        result[i2: i2 + window_size] += hanning_window*a2_rephased.real

    # normalize (16bit)
    result = ((2**(16-4)) * result/result.max())

    return result.astype('int16')

def pitchshift(snd_array, n, window_size=2**13, h=2**11):
    """ 
    Changes the pitch of a sound by ``n`` semitones. 
    
    """
    
    factor = 2**(1.0 * n / 12.0)
    stretched = stretch(snd_array, 1.0/factor, window_size, h)
    return speedx(stretched[window_size:], factor)

def parse_arguments():
    """
    Parses a file that the program uses to learn what keyboard key keys to what note

    """
    
    description = ('Use your computer keyboard as a "piano"')

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--wav', '-w',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='bowl.wav',
        help='WAV file (default: bowl.wav)')
    parser.add_argument(
        '--keyboard', '-k',
        metavar='FILE',
        type=argparse.FileType('r'),
        default='my_keyboard.kb',
        help='keyboard file (default: my_keyboard.kb)')
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='verbose mode')

    return (parser.parse_args(), parser)

def main():
    # Parse command line arguments
    (args, parser) = parse_arguments()

    # Enable warnings from scipy if requested
    if not args.verbose:
        warnings.simplefilter('ignore')

    # Reads the WAV file (Initialized file = bowl.wav)
    fps, sound = wavfile.read(args.wav.name)


    tones = range(-25, 25)
    sys.stdout.write('Transponding sound file... ')
    sys.stdout.flush()
    transposed_sounds = [pitchshift(sound, n) for n in tones]
    print('DONE')

    # Initializes the mixer module for sound loading and playback. 
    pygame.mixer.init(fps, -16, 1, 4096)
    # For the focus
    screen = pygame.display.set_mode((1000, 1000))

    # Maps the keyboard clicks to different notes on the piano
    keys = args.keyboard.read().split('\n')
    sounds = map(pygame.sndarray.make_sound, transposed_sounds)
    key_sound = dict(zip(keys, sounds))
    is_playing = {k: False for k in keys}

    while True:
        event = pygame.event.wait()

        # Press and release of the keys on the keyboard
        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            # assigns the descriptive name of the button on the keyboard to a variable 'key'
            key = pygame.key.name(event.key)

        # Press and the case of sustain (taking care of the sustain pedal effects on a piano)
        if event.type == pygame.KEYDOWN:
            if (key in key_sound.keys()) and (not is_playing[key]):
                # A short fade out effect on the sound of the note
                key_sound[key].play(fade_ms=50)
                is_playing[key] = True

            # Exception of the button 'escape' being pressed on the keyboard - quitting the program
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise KeyboardInterrupt

        elif event.type == pygame.KEYUP and key in key_sound.keys():
            # Stops with 50ms fadeout
            key_sound[key].fadeout(50)
            is_playing[key] = False

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Goodbye')