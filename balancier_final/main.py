#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 14 mars 2015

@author: christophe.bolinhas, mathieu.rosser
'''


import numpy as np
import cv2


class CenterData():
    def __init__(self, timestamp, x, y):
        self.timestamp = timestamp
        self.x = x
        self.y = y
        
    def __repr__(self):
        return "[%f] (%f,%f)\n" %(self.timestamp, self.x, self.y)

class App:
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
        self.frame = None
        self.paused = True
        self.list_centers = []
        

    def run(self):
        
        kernel_erosion = np.ones((17,17),np.uint8)
        kernel_dilatation = np.ones((13,13),np.uint8)

        while True:
            playing = True#not self.paused
            
            if playing or self.frame is None:
                ret, frame = self.cap.read()
                if not ret:
                    break
                self.frame = frame.copy()
                
            #gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            b, g, r = cv2.split(self.frame)
            
            (retVal, newImg) = cv2.threshold(b, 90, 255, cv2.THRESH_BINARY)
            
            inverse = self.invert(newImg)
            
            erosion = cv2.erode(inverse, kernel_erosion)
            dilatation = cv2.dilate(erosion, kernel_dilatation)
            
            # cv2.HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]]) -> circles
            # param1 = canny_threshold
            # param2 = accumulator
            # minDist, param2 = + ils sont petits, + il y a de faux positifs; + ils sont grands, + on rate des cercles
            circles = cv2.HoughCircles(dilatation, cv2.cv.CV_HOUGH_GRADIENT, 1, 500, np.array([]), 200, 10, 60, 3000)
            
            if circles is not None:
                print("circles")
                # convert the (x, y) coordinates and radius of the circles to integers
                circles = np.round(circles[0, :]).astype("int")
             
                # loop over the (x, y) coordinates and radius of the circles
                for (x, y, r) in circles:
                    # draw the outer circle
                    cv2.circle(self.frame,(x,y),r,(0,255,0),2)
                    # draw the center of the circle
                    cv2.circle(self.frame,(x,y),2,(255,0,0),3)
                    
                x, y, r = circles[0]
                timestamp = self.cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
                
                center_data = CenterData(timestamp, x, y)
                self.list_centers.append(center_data)

            
            #if playing:
                    
                #balancier.analyze(mean)
                    
                    #cv2.waitKey()            
            
            
            #cv2.imshow('plane', self.frame)
            #cv2.imshow('erosion', erosion)
            #cv2.imshow('dilatation', dilatation)
            #cv2.imshow('threshold', newImg)
            
            #cv2.waitKey()

            ch = cv2.waitKey(1)
            if ch == ord(' '):
                self.paused = not self.paused
            if ch == 27:
                break

        #print(self.list_centers)
        
        balancier = Balancier(self.list_centers)
        balancier.analyze()
        
    def invert(self, imagem):
        return (255-imagem)
        

class Balancier():
    
    def __init__(self, list_centers):
        self.list_centers = list_centers
        
    def analyze(self):
        list_periodes = []

        is_looking_for_left = True
        list_right_center = []
        const_counter = 4
        counter = const_counter
        current_max = None
        for center in self.list_centers:
            timestamp, x, y = center.timestamp, center.x, center.y
            if is_looking_for_left:
                if current_max is None or current_max.x > center.x:
                    current_max = center
                    counter = const_counter
                else:
                    counter-=1
            else:
                if current_max is None or current_max.x < center.x:
                    current_max = center
                    counter = const_counter
                else:
                    counter-=1
                
            if counter == 0:
                if not is_looking_for_left:
                    list_right_center.append(current_max)
                is_looking_for_left = not is_looking_for_left
                
#            if current_max is None or current
        last_center = None
        for centers_right in list_right_center:
            if last_center is not None:
                print(centers_right.timestamp - last_center.timestamp)
            last_center = centers_right    
        
        return list_periodes
    
# import time

# class Balancier():
#     
#     def __init__(self):
#         self.periode = 0
#         self.last_position = None
#         self.left_to_right = True
#         self.margin = 6
#         self.start_time = None
#         self.list_periodes = []
# 
#         
#     def analyze(self, position):
#         
#         if self.last_position is not None:
#             dx = position[0] - self.last_position[0]
#             dy = position[1] - self.last_position[1]
#             
#             #print("dx=%f" %dx)
#             
#             if self.left_to_right is True:
#                 
#                 #print("LeftToRight")
#                 
#                 if dx < - self.margin:
#                     #print("dx < -margin")
#                     
#                     if self.start_time is not None:
#                         self.periode = time.clock() - self.start_time
#                         self.list_periodes.append(self.periode)
#                         print("periode = %f" %self.periode)
#                         cv2.waitKey()
#                         
#                     self.start_time = time.clock()
#                     self.left_to_right = False
#                     
#             else:
#                 #print("RightToLeft")
#                 
#                 if dx > + self.margin:
#                     #print("dx > + margin")
#                     self.left_to_right = True
#             
#         self.last_position = position

if __name__ == '__main__':
    print __doc__

    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    App(video_src).run()

