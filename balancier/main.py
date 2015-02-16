#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 16 févr. 2015

@author: christophe.bolinhas, mathieu.rosser
'''

import cv2
import numpy as np

def manage_frame(frame):
    
    template = cv2.imread("../image/fixe.png")
    w, h = template.shape[::-1]
    
#     img = cv2.imread('messi5.jpg',0)
#     img2 = img.copy()
#     template = cv2.imread('template.jpg',0)
#     w, h = template.shape[::-1]
    
    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    for meth in methods:
        img = frame.copy()
        method = eval(meth)
    
        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)
    
        cv2.imshow("Matching Result", res)
        cv2.imshow("Detected Point", img)

def read_video(video_file):
    cap = cv2.VideoCapture(video_file)

    while cap.isOpened():
        ret, frame = cap.read()
        
        if frame is None:
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        manage_frame(gray)
        
        cv2.imshow('frame', gray)
        
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    
    read_video('../video/exemple.mp4')
    
