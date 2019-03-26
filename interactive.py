
import numpy as np
import cv2 as cv2
from threading import Thread
from music21 import *

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


class Detection(object):
    THRESHOLD = 1500

    def __init__(self, image):
        self.previous_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def get_active_cell(self, image):
        # obtain motion between previous and current image
        current_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        delta = cv2.absdiff(self.previous_gray, current_gray)
        threshold_image = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]

        # debug
        cv2.imshow('OpenCV Detection', image)
        cv2.waitKey(10)

        # store current image
        self.previous_gray = current_gray

        # set cell width
        height, width = threshold_image.shape[:2]
        cell_width = width / 7

        # store motion level for each cell
        cells = np.array([0, 0, 0, 0, 0, 0, 0])
        cells[0] = cv2.countNonZero(threshold_image[0:int(height), 0:int(cell_width)])
        cells[1] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width):int(cell_width) * 2])
        cells[2] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width) * 2:int(cell_width) * 3])
        cells[3] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width) * 3:int(cell_width) * 4])
        cells[4] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width) * 4:int(cell_width) * 5])
        cells[5] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width) * 5:int(cell_width) * 6])
        cells[6] = cv2.countNonZero(threshold_image[0:int(height), int(cell_width) * 6:int(width)])

        # obtain the most active cell
        top_cell = np.argmax(cells)

        # return the most active cell, if threshold met
        if (cells[top_cell] >= self.THRESHOLD):
            return top_cell
        else:
            return None

# musical notes (C, D, E, F, G, A, B)
NOTES = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

# initialise webcam and start thread
webcam = Webcam()
webcam.start()

# initialise detection with first webcam frame
image = webcam.get_current_frame()
detection = Detection(image)

# initialise switch
switch = True

while True:

    # get current frame from webcam
    image = webcam.get_current_frame()

    # use motion detection to get active cell
    cell = detection.get_active_cell(image)
    if cell == None: continue

    # if switch on, play note
    # Currently this weird.
    if switch:
        n = (NOTES[cell], 1000)
        n = n.Notes(str(n))
        n.show('midi')
    # alternate switch
    switch = not switch

