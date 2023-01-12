import cv2
<<<<<<< HEAD
import math
=======
>>>>>>> Initial Raspberry Pi code backup to GitHub. Includes basic apriltag discovery.
import numpy as np
import apriltag
import imutils
from apriltag import Detector
capture = cv2.VideoCapture('/dev/video1', cv2.CAP_V4L)
<<<<<<< HEAD

data_log = 'homography' #homography, id, decision margin, center

=======
>>>>>>> Initial Raspberry Pi code backup to GitHub. Includes basic apriltag discovery.
while True:
    ret, frame = capture.read()
    cv2.imshow("Output", frame)
    cv2.waitKey(1)
    frame = imutils.resize(frame, width=600)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = frame
    apriltag.DetectorOptions(families="tag16h5")
    detector = apriltag.Detector()
    detector.add_tag_family("tag16h5")
    detections = detector.detect(image)
<<<<<<< HEAD
    #if detections:
        # print(detections[0])
        #homography = detections[0].homography
        #print(str(round(homography[0][0], 2)))
        #hx = round(homography[1][0], 2)
        #hy = round(homography[1][1], 2)
        #hz = round(homography[1][2], 2)
        #fhomography = f"{str(round(homography[0][0], 2))}, {str(round(homography[0][1], 2))}, {str(round(homography[0][2], 2))}"
        #fdistance_to = str(math.sqrt(hx * hx + hy * hy + hz * hz))
        #print(fhomography)
        #print(f"Family: {str(detections[0].tag_family)}, Tag: {str(detections[0].tag_id)}, Distance of {str(detections[0].homography)} to center of {str(detections[0].center)}")
=======
>>>>>>> Initial Raspberry Pi code backup to GitHub. Includes basic apriltag discovery.
    print(detections)