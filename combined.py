# Import code lib for various commands used in the code
from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import math
from networktables import NetworkTables
import apriltag
from apriltag import Detector

# Network tables
# change server IP for the robot when added to robot, rn the server IP i s just the local address for testing
NetworkTables.initialize(server="127.0.0.1")
sd = NetworkTables.getTable("SmartDashboard")

# Begin writing varibles that do not change throughout varibles

capture = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
capture_dim = [capture.get(cv2.CAP_PROP_FRAME_WIDTH), capture.get(cv2.CAP_PROP_FRAME_HEIGHT)]
capture.set(cv2.CAP_PROP_FRAME_WIDTH, capture_dim[0])
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, capture_dim[1])
# capture.set(15, -8)

def find_cube_pos(frame):
    

    centroid = None
    
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.inRange(frame, (110, 60, 0), (135, 255, 255))
    mask_result = cv2.bitwise_and(frame, frame, mask=mask)
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
        center = (int(x + w/2), int(y + h/2))
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 255), 2)
        cv2.circle(frame, center, 4, (255,0, 255), -1)
        centroid = (cx, cy)
        
        centered_centroid = (-cx + capture_dim[0]/2, -cy + capture_dim[1]/2)
        #print(capture_dim[1]/5)
        centered_and_close = False
        if centered_centroid[0] > -20 and centered_centroid[0] < 20 and centered_centroid[1] < -capture_dim[1] / 6:
            print("cone ready for next stage")
            centered_and_close = True
        else:
            pass
            #print("cone NOT ready for next stage")
        #print(centered_centroid)
    if centroid == None:
        #print('Cube not on screen')
        sd.putValue("cube_there", False)
        return None
    else:
        print('Cube on screen')
        sd.putValue("cube_there", True)
        sd.putValue("cube_x", centered_centroid[0])
        sd.putValue("cube_y", centered_centroid[1])
        sd.putValue("cube_ready", centered_and_close)
        return [centered_centroid, centered_and_close]



def find_cone_pos(frame):
    

    centroid = None
    
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.inRange(frame, (10, 160, 0), (30, 255, 255))
    mask_result = cv2.bitwise_and(frame, frame, mask=mask)
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
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255, 0, 255), 2)
        cv2.circle(frame, center, 4, (255,0, 255), -1)
        centroid = (cx, cy)
        diff = (center[0]-centroid[0], center[1] - centroid[1])
        diff = diff/np.linalg.norm(diff)
        angle = math.atan2(diff[1], diff[0])
        extLeft = tuple(highest_cnt[highest_cnt[:, :, 0].argmin()][0])
        extRight = tuple(highest_cnt[highest_cnt[:, :, 0].argmax()][0])
        extTop = tuple(highest_cnt[highest_cnt[:, :, 1].argmin()][0])
        extBot = tuple(highest_cnt[highest_cnt[:, :, 1].argmax()][0])
        exts = [extLeft, extRight, extTop, extBot]
        largest_ext = extLeft
        for ext in exts:
            if get_vec_mag(np.subtract(ext, centroid)) > get_vec_mag(np.subtract(largest_ext, centroid)):
                largest_ext = ext
        cv2.circle(frame, largest_ext, 8, (255,0, 0), -1)
        rel_largest_ext = np.subtract(largest_ext, centroid)
        angle = math.atan2(rel_largest_ext[1], rel_largest_ext[0])
        is_upright = False
        # adjust the wh_ratio filter for when the camera is adjusted
        if wh_ratio < .8 and angle < -(math.pi/6 + math.pi /4) and angle > -(math.pi/3 + math.pi /4):
            #print('standing up')
            is_upright = True
        else:
            #print('fallen down')
            pass
        #cv2.line(frame, (cx, cy), center, (0,0, 255), 2)
        cv2.line(frame, (cx, cy), (int(cx + math.cos(angle) * 30), int(cy + math.sin(angle) * 30)), (255,0, 0), 2)
        #print(angle / math.pi * 180,  " " , wh_ratio)
        #print(wh_ratio)
        #cv2.imshow("Cone Result", inverted_result)
        centered_centroid = (-cx + capture_dim[0]/2, -cy + capture_dim[1]/2)
        #print(capture_dim[1]/5)
        centered_and_close = False
        if centered_centroid[0] > -20 and centered_centroid[0] < 20 and centered_centroid[1] < -capture_dim[1] / 6:
            #print("cone ready for next stage")
            centered_and_close = True
        else:
            #print("cone NOT ready for next stage")
            pass
        #print(centered_centroid)
    if centroid == None:
        #print('Cone not on screen')
        sd.putValue("cone_there", False)
        return None
    else:
        #print('Cone on screen')
        sd.putValue("cone_there", True)
        sd.putValue("cone_x", centered_centroid[0])
        sd.putValue("cone_y", centered_centroid[1])
        sd.putValue("cone_is_upright", is_upright)
        sd.putValue("cone_angle", angle)
        sd.putValue("cone_ready", centered_and_close)
        return [centered_centroid, is_upright, angle, centered_and_close] # angle in radians

def apriltag_detection(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    apriltag.DetectorOptions(families="tag16h5")
    detector = apriltag.Detector()
    detections = detector.detect(gray)
    if (detections):
        if (detections[0].tag_id <= 8):
            print(detections)
            tagsize = 0.152
            fx = 484.34625874
            fy = 483.97948992
            cx = 304.89078752
            cy = 236.58729305
            cameraparams = (fx,fy,cx,cy)
            pose = detector.detection_pose(detections[0], cameraparams, tagsize)
            for tag in detections:
                print(tag.tag_id)
                print(pose)
                print(pose[0][2][3])
                sd.putValue("tag_read", tag.tag_id)
                sd.putValue("Distance", pose[0][2][3])
    cv2.imshow("Grayscale", gray)
    cv2.waitKey(1)
    
    


def get_vec_mag(vec):
    return math.sqrt(vec[0] * vec[0] + vec[1] * vec[1])
# Begin repeated capture of video
while True:
    ret, frame = capture.read()
    cv2.imshow('Reg Frame', frame)
    framehsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    find_cube_pos(framehsv)
    find_cone_pos(framehsv)
    apriltag_detection(frame)
    # TO SEND BACK FROM FINDING THE CONE POS: cone centroid on screen, is cone upright,
    # cone yaw (in radians, only used if cone is not upright), is cone ready for pickup
    cv2.rectangle(framehsv, (int(capture_dim[0]/2) - 20, int(capture_dim[1]/2+capture_dim[1]/6)), (int(capture_dim[0]/2) + 20, int(capture_dim[1])), (255, 255, 255), 2)
    cv2.circle(framehsv, (int(capture_dim[0]/2), int(capture_dim[1]/2)), 4, (255,255, 255), -1)
    cv2.imshow("Frame", framehsv)
    
    cv2.waitKey(1)

