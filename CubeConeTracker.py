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
capture.set(15, -8)

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

    centroid = None
    
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.inRange(frame, (10, 160, 0), (30, 255, 255))
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
        centroid = [cx, cy]
        x,y,w,h = cv2.boundingRect(highest_cnt)
        wh_ratio = w/h
        center = (int(x + w/2), int(y + h/2))
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 255, 255), 2)
        cv2.circle(frame, center, 4, (255,255, 255), -1)
        centroid = (cx, cy)
        diff = (center[0]-centroid[0], center[1] - centroid[1])
        diff = diff/np.linalg.norm(diff)
        #print(diff)
        angle = math.atan2(diff[1], diff[0])
        angle_deg = angle / math.pi * 180
        extLeft = tuple(highest_cnt[highest_cnt[:, :, 0].argmin()][0])
        extRight = tuple(highest_cnt[highest_cnt[:, :, 0].argmax()][0])
        extTop = tuple(highest_cnt[highest_cnt[:, :, 1].argmin()][0])
        extBot = tuple(highest_cnt[highest_cnt[:, :, 1].argmax()][0])
        extAll = tuple(highest_cnt[highest_cnt[0, 0, 0].argmax()][0])
        cv2.circle(frame, extLeft, 4, (0,255, 255), -1)
        cv2.circle(frame, extRight, 4, (0,255, 255), -1)
        cv2.circle(frame, extTop, 4, (0,255, 255), -1)
        cv2.circle(frame, extBot, 4, (0,255, 255), -1)
        cv2.circle(frame, extAll, 6, (255,255, 255), -1)
        # this ratio should be > 1 if the width is greater than the height and < 1 if height is greater than 1
        if wh_ratio > 1:
            #print('fallen down and pointing with 45 degrees of to the left or right of the camera')
            pass
        else:
            #print('standing up or fallen down but within 45 degrees of yaw of being pointed away or at the camera')
            pass
        cv2.line(frame, (cx, cy), center, (0,0, 255), 2)
        #cv2.line(frame, (cx, cy), (int(cx + math.cos(angle) * 40), int(cy + math.sin(angle) * 40)), (0,0, 255), 2)
        print(angle_deg)
            
            
    cv2.imshow("Cone Result", inverted_result)
    
    if centroid == None:
        #print('Cube not on screen')
        return None
    else:
        #print(pos_of_rel_center)
        #sender.send_cone_data([True, pos_of_rel_center[0], pos_of_rel_center[1]])
        return centroid

# Begin repeated capture of video
while True:
    ret, frame = capture.read()
    framehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    #find_cube_pos(frame)
    find_cone_pos(framehsv)
    cv2.imshow("Frame", framehsv)
    
    cv2.waitKey(1)

