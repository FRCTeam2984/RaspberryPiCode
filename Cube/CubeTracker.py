# Import code lib for various commands used in the code
from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils

greenBGR = np.uint8([[[0,255,0 ]]])
 
hsv_green = cv2.cvtColor(greenBGR,cv2.COLOR_BGR2HSV)
print (hsv_green)
# Begin writing varibles that do not change throughout varibles

capture = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)


# Begin repeated capture of video
while True:
    ret, frame = capture.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    result = frame.copy()
    # mask = cv2.inRange()
    # lower boundary RED color range values; Hue (0 - 10)
    #lower1 = np.array([0, 100, 20])
    #upper1 = np.array([10, 255, 255])
     
    # upper boundary RED color range values; Hue (160 - 180)
    #lower2 = np.array([160,100,20])
    #upper2 = np.array([179,255,255])
     
    #lower_mask = cv2.inRange(frame, lower1, upper1)
    #upper_mask = cv2.inRange(frame, lower2, upper2)
     
    #full_mask = lower_mask + upper_mask;
    kernel = np.ones((5, 5), np.uint8)
    full_mask = cv2.inRange(frame, (110, 80, 0), (130, 255, 255))
    result = cv2.bitwise_and(result, result, mask=full_mask)
    eroded_mask = cv2.erode(full_mask, kernel, cv2.BORDER_REFLECT)
    h, s, v = frame[:, :, 0], frame[:, :, 1], frame[:, :, 2]
    #image = cv2.circle(image, (x,y), radius=0, color=(0, 0, 255), thickness=-1)
    # cv2.imshow("masked", masked_img)
    ret,thresh = cv2.threshold(full_mask,127,255,0)
     
    # calculate moments of binary image
    M = cv2.moments(thresh)
    
    # calculate x,y coordinate of center
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    
    # put text and highlight the center
    cv2.circle(eroded_mask, (cX, cY), 5, (155, 155, 155), -1)
    cv2.putText(eroded_mask, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (155, 155, 155), 2)
    
    cv2.imshow('result', eroded_mask)
    #cv2.imshow("Hue", h)
    #cv2.imshow("Satuation", s)
    cv2.waitKey(1)
