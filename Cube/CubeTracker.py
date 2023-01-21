# Import code lib for various commands used in the code
from collections import deque
from imutils.video import VideoStream
from networktables import NetworkTables
import numpy as np
import cv2
import imutils

greenBGR = np.uint8([[[0,255,0 ]]])
 
hsv_green = cv2.cvtColor(greenBGR,cv2.COLOR_BGR2HSV)
print (hsv_green)
# Begin writing varibles that do not change throughout varibles

capture = cv2.VideoCapture('/dev/video1', cv2.CAP_V4L)


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
    full_mask = cv2.inRange(frame, (120, 50, 20), (140, 150, 255))
    result = cv2.bitwise_and(result, result, mask=full_mask)
     
    cv2.imshow('mask', full_mask)
    cv2.imshow('result', result)
    cv2.imshow("Capture", frame)
    cv2.waitKey(1)
