""" Experiment with face detection and image filtering using OpenCV

Author: SPARSH BANSAL
"""

import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
#kernel = np.ones((11, 11), 'uint8')
kernel = np.ones((40, 40), 'uint8')

cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20, 20))
    for (x, y, w, h) in faces:
        frame[y:y+h, x:x+w, :] = cv2.dilate(frame[y:y+h, x:x+w, :], kernel)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255))
        #Drawing circles for the eyeballs
        cv2.circle(frame, (int(x+w/4) , int(y+h/2.8)), 20, (255,255,255), -1)
        cv2.circle(frame, (int(x+w/4) , int(y+h/2.6)), 10, (0,0,0), -1)
        cv2.circle(frame, (int(x+w/1.4) , int(y+h/2.6)), 20, (255,255,255), -1)
        cv2.circle(frame, (int(x+w/1.4) , int(y+h/2.4)), 10, (0,0,0), -1)
        #Drawing an ellipse for the lips and mouth
        cv2.ellipse(frame, (int(x+w/1.8) , int(y+h/1.3)), (int(0.3*w), int(0.1*h)) , 0, 0, 180, (0,0,0), 4)
    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
