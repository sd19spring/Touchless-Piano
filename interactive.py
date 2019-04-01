
import numpy as np
import cv2 as cv2
from threading import Thread
from music21 import *


#Makes a new class called webcam which captures current frames
class Webcam:

    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.current_frame = self.video_capture.read()[1]

    # create thread for capturing images
    def start(self):
        Thread(target=self._update_frame, args=()).start()

    def _update_frame(self):
        while (True):
            self.current_frame = self.video_capture.read()[1]

    # get the current frame
    def get_current_frame(self):
        return self.current_frame


# Makes a class called Detection which detects motion by comparing frames
class Detection(object):
    THRESHOLD = 1500

    def __init__(self, image):
        self.previous_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def get_active_cell(self, image):
        # obtain motion between previous and current image
        current_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        delta = cv2.absdiff(self.previous_gray, current_gray)
        threshold_image = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]

        # delays by a few frames for better input
        cv2.imshow('OpenCV Detection', image)
        cv2.waitKey(100)

        # stores current image
        self.previous_gray = current_gray

        # sets cell width
        height, width = threshold_image.shape[:2]
        cell_width = width / 9

        # store motion level for each cell
        cells = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])
        cells[0] = cv2.countNonZero(threshold_image[0:int(height), 0:int(cell_width)])
        cells[1] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width):int(cell_width) * 2])
        cells[2] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width) * 2:int(cell_width) * 3])
        cells[3] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width) * 3:int(cell_width) * 4])
        cells[4] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width) * 4:int(cell_width) * 5])
        cells[5] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width) * 5:int(cell_width) * 6])
        cells[6] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width) * 6:int(width)]*7)
        cells[7] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width) * 7:int(width)]*8)
        cells[8] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width) * 8:int(width)])

        # obtain the most active cell
        top_cell = np.argmax(cells)

        # return the most active cell, if threshold met
        if cells[top_cell] >= self.THRESHOLD:
            return top_cell
        else:
            return None

# list of notes
note.list = ['C', 'D', 'E', 'F', 'G', 'A', 'B', '-', '#']

# starts webcam and thread
webcam = Webcam()
webcam.start()

# begins detection with the first webcam frame
image = webcam.get_current_frame()
detection = Detection(image)

# switches on if movement is detected
switch = True

while True:

    # gets current frame from the webcam
    image = webcam.get_current_frame()

    # uses motion detection to retrieve active cell
    cell = detection.get_active_cell(image)
    if cell == None: continue

    # if the switch is on, plays the selected note
    if switch:
        if note.list[cell] != '-' and note.list[cell] != '#':
            n = note.list[cell]
            print(n)
        elif note.list[cell] == '-' or note.list[cell] == '#':
            sf = note.list[cell]
            n = str(input("what note do you want")) + str(note.list[cell])
            print(n)
        n = note.Note(str(n.upper()))
        n.show('midi')
    # alternate switch
    switch = not switch

def playnote():
    oknotes = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    n = input("Press select which note you would like to play!")
    sf = input("Is the note sharp or flat? Hold finger over the s for sharp, f for flat, or another button for neither.")
    if n.lower() in oknotes:
        if sf == 's':
            n = n + '#'
        if sf == 'f':
            n = n + "-"
        n = note.Note(str(n.upper()))
        n.duration.type = 'whole'
        return n.show('midi')
    else:
        return "Error: Out of Range. Please input a letter between A and G, or C5."