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
            #timestamp, x, y = center.timestamp, center.x, center.y
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

if __name__ == '__main__':
    pass

