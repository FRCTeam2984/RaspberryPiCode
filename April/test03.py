# Import the required libraies for the code to function
import cv2
import math
import numpy as np
import apriltag
import imutils
from apriltag import Detector
# Define Varibles
capture = cv2.VideoCapture('/dev/video1', cv2.CAP_V4L)

data_log = 'homography' #homography, id, decision margin, center

while True:
    ret, frame = capture.read()
    cv2.imshow("Output", frame)
    cv2.waitKey(1)
    frame = imutils.resize(frame, width=600)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    apriltag.DetectorOptions(families="tag16h5")
    detector = apriltag.Detector()
    detections = detector.detect(frame)
    if (detections):
        if (detections[0].tag_id <= 8):
            print(detections)
