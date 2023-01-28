# Import code lib for various commands used in the code
from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import math
  
# Begin writing varibles that do not change throughout varibles

capture = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
capture.set(3, 480)
capture.set(4, 360)

def find_cube_pos(frame):
    frame_copy = frame.copy()

    pos_of_cube_rel_center = None
    
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.inRange(frame, (110, 60, 0), (135, 255, 255))
    mask_result = cv2.bitwise_and(frame_copy, frame_copy, mask=mask)
    eroded_result = cv2.erode(mask, kernel, cv2.BORDER_REFLECT)
    inverted_result = cv2.bitwise_not(eroded_result)
    #h, s, v = frame[:, :, 0], frame[:, :, 1], frame[:, :, 2]

    contours, hier = cv2.findContours(eroded_result,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    highest_cnt_area = 0
    highest_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > highest_cnt_area and 30000 > area > 1000:
            highest_cnt = cnt
            highest_cnt_area = cv2.contourArea(cnt)
            
    M = cv2.moments(highest_cnt)
    #highest_cnt_area = cv2.contourArea(highest_cnt)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.drawContours(frame, [highest_cnt], -1, (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 4, (0,255, 0), -1)
        pos_of_cube_rel_center = [-480/2 + cx, 360/2 - cy]
    
    if pos_of_cube_rel_center == None:
        print('Cube not on screen')
        return None
    else:
        print(pos_of_cube_rel_center)
        #sender.send_cube_data([True, pos_of_cube_rel_center[0], pos_of_cube_rel_center[1]])
        return pos_of_cube_rel_center

def find_cone_pos(frame):
    frame_copy = frame.copy()

    pos_of_rel_center = None
    
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.inRange(frame, (10, 30, 50), (35, 255, 255))
    mask_result = cv2.bitwise_and(frame_copy, frame_copy, mask=mask)
    eroded_result = cv2.erode(mask, kernel, cv2.BORDER_REFLECT)
    inverted_result = cv2.bitwise_not(eroded_result)
    #h, s, v = frame[:, :, 0], frame[:, :, 1], frame[:, :, 2]

    contours, hier = cv2.findContours(eroded_result,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    highest_cnt_area = 0
    highest_cnt = None
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > highest_cnt_area and 30000 > area > 1000:
            highest_cnt = cnt
            highest_cnt_area = cv2.contourArea(cnt)
            
    M = cv2.moments(highest_cnt)
    #highest_cnt_area = cv2.contourArea(highest_cnt)
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cv2.drawContours(frame, [highest_cnt], -1, (255, 0, 0), 2)
        cv2.circle(frame, (cx, cy), 4, (255,0, 0), -1)
        pos_of_rel_center = [-480/2 + cx, 360/2 - cy]
        x,y,w,h = cv2.boundingRect(highest_cnt)
        wh_ratio = w/h
        # this ratio should be > 1 if the width is greater than the height and < 1 if height is greater than 1
        if wh_ratio > 1:
            #print('fallen down and pointing with 45 degrees of to the left or right of the camera')
            left_vector = [math.sqrt(w * h), 0]
            left_vector = left_vector/np.linalg.norm(left_vector)
            cone_vector = [w,h]
            cone_vector = cone_vector/np.linalg.norm(cone_vector)
            dt_product = np.dot(left_vector, cone_vector)
            dt_product = left_vector[0] * cone_vector[0] + left_vector[1] * cone_vector[1]
            print(dt_product)
        else:
            #print('standing up or fallen down but within 45 degrees of yaw of being pointed away or at the camera')
            up_vector = [[0, 0], [0, 1]]
            cone_vector = [[w,h], [0, 0]]
            
            
    cv2.imshow("Cone Result", inverted_result)
    
    if pos_of_rel_center == None:
        #print('Cube not on screen')
        return None
    else:
        #print(pos_of_rel_center)
        #sender.send_cone_data([True, pos_of_rel_center[0], pos_of_rel_center[1]])
        return pos_of_rel_center

# Begin repeated capture of video
while True:
    ret, frame = capture.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #find_cube_pos(frame)
    find_cone_pos(frame)
    cv2.imshow("Frame", frame)
    
    cv2.waitKey(1)

