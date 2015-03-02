'''
Created on 2 mars 2015

@author: mathieu.rosser
'''

import numpy as np
import cv2
from matplotlib import pyplot as plt

def manage_frame(gray, ref):
        
    # Initiate STAR detector
    orb = cv2.ORB()
    
    # find the keypoints with ORB
    kp = orb.detect(gray,None)
    
    # compute the descriptors with ORB
    kp, des = orb.compute(gray, kp)
    
    # draw only keypoints location,not size and orientation
    img = cv2.drawKeypoints(gray,kp,color=(0,255,0), flags=0)
    plt.imshow(img),plt.show()

if __name__ == '__main__':
    
    cap = cv2.VideoCapture(0)

    ref = cv2.imread("FixedSmall.png", 0)

    while cap.isOpened():
        ret, frame = cap.read()
        
        if frame is None:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        manage_frame(gray, ref)
        
        #cv2.imshow('frame', gray)
        
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    
