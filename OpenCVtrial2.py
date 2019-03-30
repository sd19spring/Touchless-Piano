#importing Modules

import cv2
import numpy as np

#Capturing Video through webcam.

cap = cv2.VideoCapture(0)

while(True):
        ret, frame = cap.read()

        #converting frames from RGB (Red-Green-Blue) to HSV (hue-saturation-value)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        #defining the range of Red color
        lower_red = np.array([0, 100, 100])
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
            if(area>300):    
                #finds the coordinates of the region
                x,y,w,h = cv2.boundingRect(contour) 
                #draws a frame around the region    
                frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,255),3)
                #gives the coordinates of the finger
                fx = x + w/2;
                fy = y + h/2;
                print(fx)
                print(fy)

        #Shows the video being captured, frame by frame                
        cv2.imshow("Finger Tracking",frame)
        frame = cv2.flip(frame,1)
        #Shows the masked region
        cv2.imshow("Yellow",res)
                               
        if cv2.waitKey(10) & 0xFF == 27:
                break

# releases the video capture to pause the collection
cap.release()
cv2.destroyAllWindows() 