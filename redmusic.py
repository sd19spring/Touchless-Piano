# imports Modules

import cv2
import numpy as np
from music21 import *

# Sets environment for midi, default location for timidity
environment.set('midiPath', '/usr/bin/timidity')

# Captures Video through the user's webcam
cap = cv2.VideoCapture(0)
# cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, 800)
# cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 600)

while(True):
        ret, frame = cap.read()

        # converts frames from RGB (Red-Green-Blue) to HSV (hue-saturation-value)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # defines the range of Red color in RGB values
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])

        # finds the threshold range of red colour in the image
        red = cv2.inRange(hsv, lower_red, upper_red)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame, frame, mask=red)

        # Tracks the color red
        (contours, hierarchy) = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Indexes to the contours
        for picture, contour in enumerate(contours):
            # finds the area of the contour region
            area = cv2.contourArea(contour)
            # finds the coordinates of the region
            x, y, w, h = cv2.boundingRect(contour)
            # draws a frame around the region
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),3)
            # gives the coordinates of the finger
            fx = x + w/2
            fy = y - h/2
            # print(fx)
            # print(fy)
            # tracks the piano keys
            key_width = 53
            # B note
            if fx <= 53:
                n = 'B'
                n = note.Note(str(n))
                n.show('midi')
            # A# note
            if 54 <= fx <= 106:
                n = 'A#'
                n = note.Note(str(n))
                n.show('midi')
            # A note
            if 107 <= fx <= 159:
                n = 'A'
                n = note.Note(str(n))
                n.show('midi')
            # G# note
            if 160 <= fx <= 212:
                n = 'G#'
                n = note.Note(str(n))
                n.show('midi')
            # G note
            if 213 <= fx <= 265:
                n = 'G'
                n = note.Note(str(n))
                n.show('midi')
            # F# note
            if 267 <= fx <= 318:
                n = 'F#'
                n = note.Note(str(n))
                n.show('midi')
            # F note
            if 319 <= fx <= 371:
                n = 'F'
                n = note.Note(str(n))
                n.show('midi')
            # E note
            if 372 <= fx <= 424:
                n = 'E'
                n = note.Note(str(n))
                n.show('midi')
            # D# note
            if 425 <= fx <= 477:
                n = 'D#'
                n = note.Note(str(n))
                n.show('midi')
            # D note
            if 478 <= fx <= 530:
                n = 'D'
                n = note.Note(str(n))
                n.show('midi')
            # C# note
            if 531 <= fx <= 583:
                n = 'C#'
                n = note.Note(str(n))
                n.show('midi')
            # C note
            if 584 <= fx <= 636:
                n = 'C'
                n = note.Note(str(n))
                n.show('midi')
            # Out of range; plays rest instead of stopping for an error
            else:
                n = note.Rest(type='whole')
                n.show('midi')


        # Shows the video being captured frame by frame
        cv2.imshow("Finger Tracking", frame)
        frame = cv2.flip(frame, 1)
        # Shows the masked region
        cv2.imshow("Red", res)

        if cv2.waitKey(100) & 0xFF == 27:
                break

# releases the video capture to pause the collection
cap.release()
cv2.destroyAllWindows()


# NB: I tried including code here that could help close the window without errors.
# It unfortunately did not work. If you are stuck, press ctrl + c repeatedly
# until it force quits
