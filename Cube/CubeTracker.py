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
    pos_of_cube_rel_center = [640/2, 480/2]
    
    kernel = np.ones((4, 4), np.uint8)
    mask = cv2.inRange(frame, (110, 80, 0), (130, 255, 255))
    mask_result = cv2.bitwise_and(frame_copy, frame_copy, mask=mask)
    eroded_result = cv2.erode(mask, kernel, cv2.BORDER_REFLECT)
    inverted_result = cv2.bitwise_not(eroded_result)
    #h, s, v = frame[:, :, 0], frame[:, :, 1], frame[:, :, 2]
    # Show keypoints
    contours, hier = cv2.findContours(eroded_result,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    highest_cnt_area = 0
    highest_cnt = None
    for cnt in contours:
        if cv2.contourArea(cnt) > highest_cnt_area and cv2.contourArea(cnt) > 1000:
            highest_cnt = cnt
            # print(cnt)
            #cv2.drawContours(inverted_result,[cnt],0,(0,255, 0),2)
            #cv2.drawContours(inverted_result,[cnt],0,255,-1)
    
    M = cv2.moments(highest_cnt)
    highest_cnt_area = cv2.contourArea(cnt)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.drawContours(frame, [highest_cnt], -1, (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 7, (0,255, 0), -1)
    pos_of_cube_rel_center = [-640/2 + cx, 480/2 - cy]
    
    cv2.imshow("Frame", frame)
    cv2.imshow("Keypoints", inverted_result)
    
    print(pos_of_cube_rel_center)
    cv2.waitKey(1)
