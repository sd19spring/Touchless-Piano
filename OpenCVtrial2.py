#importing Modules

import cv2
import numpy as np

#Capturing Video through webcam.
cap = cv2.VideoCapture(0)
#cap.set(cv.CV_CAP_PROP_FRAME_WIDTH, 800)
#cap.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 600)

while(True):
        ret, frame = cap.read()

        #converting frames from RGB (Red-Green-Blue) to HSV (hue-saturation-value)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #defining the range of Red color
        lower_red = np.array([0, 120, 120])
        upper_red = np.array([179, 255, 255])

        #finding the threshold range of red colour in the image
        red = cv2.inRange(hsv, lower_red, upper_red)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= red)

        #Tracking Colour (Red) 
        (contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        
        #indexing to the countours
        for picture, contour in enumerate(contours):
            # finds the area of the contour region
            area = cv2.contourArea(contour)
            #finds the coordinates of the region
            x,y,w,h = cv2.boundingRect(contour)         
            #draws a frame around the region    
            frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),3)
            #gives the coordinates of the finger
            fx = x + w/2
            fy = y - h/2
            #print(fx)
            #print(fy)
            #tracking the piano keys
            key_width = 53
            #B note
            if fx <= 53:
                print('B')
            #A# note
            if 54 <= fx <= 106:
                print('A#')
            #A note
            if 107 <= fx <= 159:
                print('A')
            #G# note
            if 160 <= fx <= 212:
                print('G#')
            #G note
            if 213 <= fx <= 265:
                print('G')
            #F# note
            if 267 <= fx <= 318:
                print('F#')
            #F note
            if 319 <= fx <= 371:
                print('F')
            #E note
            if 372 <= fx <= 424:
                print('E')
            #D# note
            if 425 <= fx <= 477:
                print('D#')
            #D note
            if 478 <= fx <= 530:
                print('D')
            #C# note
            if 531 <= fx <= 583:
                print('C#')
            #C note
            if 584 <= fx <= 636:
                print('C')
            #Out of range
            else:
                print('Out of playing range!')

        #Shows the video being captured, frame by frame                
        cv2.imshow("Finger Tracking",frame)
        frame = cv2.flip(frame,1)
        #Shows the masked region
        cv2.imshow("Red",res)
                               
        if cv2.waitKey(10) & 0xFF == 27:
                break

# releases the video capture to pause the collection
cap.release()
cv2.destroyAllWindows() 