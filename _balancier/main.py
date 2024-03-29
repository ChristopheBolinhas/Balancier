#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 14 mars 2015

@author: christophe.bolinhas, mathieu.rosser
'''


import numpy as np
import cv2

# local modules
import video
import common
from common import getsize, draw_keypoints
from plane_tracker import PlaneTracker


class App:
    def __init__(self, src):
        self.cap = video.create_capture(src)
        self.frame = None
        self.paused = True
        self.tracker = PlaneTracker()

        cv2.namedWindow('plane')
        self.rect_sel = common.RectSelector('plane', self.on_rect)

    def on_rect(self, rect):
        self.tracker.clear()
        self.tracker.add_target(self.frame, rect)

    def run(self):
        balancier = Balancier()
        
        while True:
            playing = not self.paused and not self.rect_sel.dragging
            if playing or self.frame is None:
                ret, frame = self.cap.read()
                if not ret:
                    break
                self.frame = frame.copy()

            w, h = getsize(self.frame)
            vis = np.zeros((h, w*2, 3), np.uint8)
            vis[:h,:w] = self.frame
            if len(self.tracker.targets) > 0:
                target = self.tracker.targets[0]
                vis[:,w:] = target.image
                draw_keypoints(vis[:,w:], target.keypoints)
                x0, y0, x1, y1 = target.rect
                cv2.rectangle(vis, (x0+w, y0), (x1+w, y1), (0, 255, 0), 2)

            if playing:
                tracked = self.tracker.track(self.frame)
                #print(len(tracked))
                if len(tracked) > 0:
                    tracked = tracked[0]
                    cv2.polylines(vis, [np.int32(tracked.quad)], True, (255, 255, 255), 2)
                    
                    sum =  [0, 0]
                    
                    for (x0, y0), (x1, y1) in zip(np.int32(tracked.p0), np.int32(tracked.p1)):
                        cv2.line(vis, (x0+w, y0), (x1, y1), (0, 255, 0))
                        
                        sum[0] += x1
                        sum[0] += y1
                        
                    length = len(tracked.p1)
                    mean = (sum[0] / length, sum[1] / length)
                    
                    balancier.analyze(mean)
                    
                    #cv2.waitKey()
                    
                draw_keypoints(vis, self.tracker.frame_points)
            
            #cv2.waitKey()
            
            self.rect_sel.draw(vis)
            cv2.imshow('plane', vis)
            ch = cv2.waitKey(1)
            if ch == ord(' '):
                self.paused = not self.paused
            if ch == 27:
                break

import time

class Balancier():
    
    def __init__(self):
        self.periode = 0
        self.last_position = None
        self.left_to_right = True
        self.margin = 6
        self.start_time = None
        self.list_periodes = []

        
    def analyze(self, position):
        
        if self.last_position is not None:
            dx = position[0] - self.last_position[0]
            dy = position[1] - self.last_position[1]
            
            #print("dx=%f" %dx)
            
            if self.left_to_right is True:
                
                #print("LeftToRight")
                
                if dx < - self.margin:
                    #print("dx < -margin")
                    
                    if self.start_time is not None:
                        self.periode = time.clock() - self.start_time
                        self.list_periodes.append(self.periode)
                        print("periode = %f" %self.periode)
                        cv2.waitKey()
                        
                    self.start_time = time.clock()
                    self.left_to_right = False
                    
            else:
                #print("RightToLeft")
                
                if dx > + self.margin:
                    #print("dx > + margin")
                    self.left_to_right = True
            
        self.last_position = position

if __name__ == '__main__':
    print __doc__

    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
    App(video_src).run()

