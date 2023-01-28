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
capture.set(3, 640)
capture.set(4, 480)

# Begin repeated capture of video
while True:
    ret, frame = capture.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_copy = frame.copy()
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
    kernel = np.ones((2, 2), np.uint8)
    mask = cv2.inRange(frame, (110, 80, 0), (130, 255, 255))
    mask_result = cv2.bitwise_and(frame_copy, frame_copy, mask=mask)
    eroded_result = cv2.erode(mask, kernel, cv2.BORDER_REFLECT)
    inverted_result = cv2.bitwise_not(eroded_result)
    #h, s, v = frame[:, :, 0], frame[:, :, 1], frame[:, :, 2]
    #image = cv2.circle(image, (x,y), radius=0, color=(0, 0, 255), thickness=-1)
    retval, threshold = cv2.threshold(inverted_result, 200, 255, cv2.THRESH_BINARY_INV)
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 10;
    params.maxThreshold = 400;
     
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 1500
     
    # Filter by Circularity
    params.filterByCircularity = False
    params.minCircularity = 0.1
     
    # Filter by Convexity
    params.filterByConvexity = False
    params.minConvexity = 0.87
     
    # Filter by Inertia
    params.filterByInertia = False
    params.minInertiaRatio = 0.01

    detector = cv2.SimpleBlobDetector_create(params)

    # Set up the detector with default parameters.
    #detector = cv2.SimpleBlobDetector()

    # Detect blobs.
    keypoints = detector.detect(inverted_result)
    print(keypoints)
    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(inverted_result, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Show keypoints
    cv2.imshow("Keypoints", im_with_keypoints)
    # calculate moments of binary image
    # M = cv2.moments(thresh)
    # print(M)
    # calculate x,y coordinate of center
    #fix division by 0 error (IMPORTANT)
    # cX = int(M["m10"] / M["m00"])
    # cY = int(M["m01"] / M["m00"])
    
    # put text and highlight the center
    # cv2.circle(inverted_result, (cX, cY), 5, (155, 155, 155), -1)
    # cv2.putText(inverted_result, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (155, 155, 155), 2)
    
    # cv2.imshow('result', inverted_result)
    cv2.waitKey(1)
