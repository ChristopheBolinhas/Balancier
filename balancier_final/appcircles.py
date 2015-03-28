#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Application de calcul de mouvements de balancier
Analyse de vidéo de balancier avec des cercles de couleurs RGB et Hough
@author: christophe.bolinhas, mathieu.rosser
'''

import numpy as np
import cv2
from balancier import Balancier, CenterData


class AppCircles():
    ''' Classe analysant une vidéo d'un cercle R/G/B en balanchement, 
        en utilisant un seuillage, une séparation de couleur RGB, une ouverture et Hough '''
    
    def __init__(self, src, color = "R", show_video = False):
        self.color = color if color in "RGB" else "R"
        self.show_video = show_video
        
        self.window_threshold, self.window_dilation, self.window_hough  = 'Seuillage', 'Dilation apres inversion et erosion', 'Analyse balancier par cercle Hough'
        cv2.namedWindow(self.window_threshold)
        cv2.namedWindow(self.window_dilation)
        cv2.namedWindow(self.window_hough)
        cv2.moveWindow(self.window_threshold, 0, 0)
        cv2.moveWindow(self.window_dilation, 850, 0)
        cv2.moveWindow(self.window_hough, 0, 450)
        
        self.cap = cv2.VideoCapture(src)
        self.frame = None
        self.paused = True
        self.list_centers = []        

    def run(self):
        ''' exécution de l'analyse video '''
        
        kernel_erosion = np.ones((17,17),np.uint8)
        kernel_dilatation = np.ones((13,13),np.uint8)

        while True:
            playing = True
            
            if playing or self.frame is None:
                ret, frame = self.cap.read()
                if not ret:
                    break
                self.frame = frame.copy()
            
            # séparation R/G/B et seuillage   
            b, g, r = cv2.split(self.frame)
            ch = b if self.color in "RG" else r
            
            (retVal, img_threshold) = cv2.threshold(ch, 90, 255, cv2.THRESH_BINARY)
            
            # ouverture
            inverse = self.invert(img_threshold)
            erosion = cv2.erode(inverse, kernel_erosion)
            dilatation = cv2.dilate(erosion, kernel_dilatation)
            
            # recherche de cercles Hough
            # cv2.HoughCircles(image, method, dp, minDist[, circles[, param1[, param2[, minRadius[, maxRadius]]]]]) -> circles
            # param1 = canny_threshold
            # param2 = accumulator
            # minDist, param2 = + ils sont petits, + il y a de faux positifs; + ils sont grands, + on rate des cercles
            circles = cv2.HoughCircles(dilatation, cv2.cv.CV_HOUGH_GRADIENT, 1, 500, np.array([]), 200, 10, 60, 3000)
            
            if circles is not None:
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
                
                # ajout des données balancier
                center_data = CenterData(timestamp, x, y)
                self.list_centers.append(center_data)            
            
            if self.show_video:
                cv2.imshow(self.window_threshold, img_threshold)
                cv2.imshow(self.window_dilation, dilatation)
                cv2.imshow(self.window_hough, self.frame)
            
            ch = cv2.waitKey(1)
            if ch == ord(' '):
                self.paused = not self.paused
            if ch == 27:
                break
        
        # analyse balancier
        return Balancier(self.list_centers).analyze()
        
    def invert(self, imagem):
        return (255-imagem)
    

if __name__ == '__main__':
    pass

