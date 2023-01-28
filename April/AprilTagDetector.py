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
            # print(detections)
            homography = detections[0].homography
            corners = detections[0].corners
            topr_c = np.array(corners[1])
            topl_c = np.array(corners[0])
            bottomr_c = np.array(corners[2])
            bottoml_c = np.array(corners[3])
            middlel = (bottoml_c + topl_c) /2#[(bottoml_c[0] + topl_c[0])/2, (bottoml_c[1] + topl_c[1])/2]
            middler = (bottomr_c + topr_c) /2#[(bottomr_c[0] + topr_c[0])/2, (bottomr_c[1] + topr_c[1])/2]
            middle_top = (topr_c + topl_c) /2#[(bottoml_c[0] + topl_c[0])/2, (bottoml_c[1] + topl_c[1])/2]
            middle_bottom = (bottomr_c + bottoml_c) /2#[(bottomr_c[0] + topr_c[0])/2, (bottomr_c[1] + topr_c[1])/2]
            height_avg = np.subtract(middle_bottom, middle_top)[1]
            length_avg = np.subtract(middler, middlel)[0]
            #yaw_deg = math.acos(length_avg, height_avg) * 180/math.pi
            if height_avg != 0 and abs(length_avg) <= abs(height_avg):
                yaw_deg = math.acos(length_avg/abs(height_avg)) * 180 / math.pi
                if middlel[1] < middler[1]:
                    yaw_deg = -yaw_deg
                print(yaw_deg)
            #print(f"height: {str(height_avg)}, length: {str(length_avg)}")
            #print(yaw_deg)
            
            
            #print(homography)
            
