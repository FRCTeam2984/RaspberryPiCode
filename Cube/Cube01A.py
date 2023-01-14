# Import code lib for various commands used in the code
from collections import deque
from imutils.video import VideoStream
from networktables import NetworkTables
import numpy as np
import cv2
import imutils

# Begin writing varibles that do not change throughout varibles

capture = cv2.VideoCapture('/dev/video1', cv2.CAP_V4L)


# Begin repeated capture of video
while True:
    ret, frame = capture.read()
    
    
    cv2.imshow("Capture", frame)
    cv2.waitKey(1)