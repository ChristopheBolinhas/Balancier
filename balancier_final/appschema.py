#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 14 mars 2015

@author: christophe.bolinhas, mathieu.rosser
'''


import numpy as np
import cv2
from common import getsize, draw_keypoints, RectSelector
from plane_tracker import PlaneTracker
from balancier import Balancier, CenterData


class AppSchema():
    def __init__(self, src_video):
        self.cap = cv2.VideoCapture(src_video)
        self.frame = None
        self.paused = True
        self.tracker = PlaneTracker()
        
        self.window_name = 'Analyse balancier par schema ORB'

        cv2.namedWindow(self.window_name)
        self.rect_sel = RectSelector(self.window_name, self.on_rect)
        
        self.list_centers = []
        print("Exemple avec détection de motif simple, algorithme : Orb")


    def on_rect(self, rect):
        self.tracker.clear()
        self.tracker.add_target(self.frame, rect)

    def run(self):
        
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
            else:
                self.paused = True
                
            tracked = self.tracker.track(self.frame)
            draw_keypoints(vis, self.tracker.frame_points)

            if playing and len(tracked) > 0:
                tracked = tracked[0]
                cv2.polylines(vis, [np.int32(tracked.quad)], True, (255, 255, 255), 2)
                
                sumXY = [0, 0]
                
                for (x0, y0), (x1, y1) in zip(np.int32(tracked.p0), np.int32(tracked.p1)):
                    cv2.line(vis, (x0+w, y0), (x1, y1), (0, 255, 0))
                    
                    sumXY[0] += x1
                    sumXY[0] += y1
                    
                length = len(tracked.p1)
                mean = (sumXY[0] / length, sumXY[1] / length)
                
                timestamp = self.cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
            
                center_data = CenterData(timestamp, mean[0], mean[1])
                self.list_centers.append(center_data)
                                
            self.rect_sel.draw(vis)
            cv2.imshow(self.window_name, vis)
            ch = cv2.waitKey(1)
            if ch == ord(' '):
                self.paused = not self.paused
            if ch == 27:
                break
            
        return Balancier(self.list_centers).analyze()

if __name__ == '__main__':
    pass

