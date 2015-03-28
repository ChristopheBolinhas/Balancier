#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Application de calcul de mouvements de balancier
Analyse de vidéo de balancier avec tracking d'un motif sélectionné par l'utilisateur et détecté avec ORB
Basé sur exemple OpenCV feature-homography
@author: christophe.bolinhas, mathieu.rosser
'''

import numpy as np
import cv2
from common import getsize, draw_keypoints, RectSelector
from plane_tracker import PlaneTracker
from balancier import Balancier, CenterData

class AppSchema():
    ''' Classe analysant une vidéo par sélection d'un schéma de référence puis tracking avec détection ORB '''
    
    def __init__(self, src_video):
        self.cap = cv2.VideoCapture(src_video)
        self.frame = None
        self.paused = True
        self.tracker = PlaneTracker()
        
        self.window_name = 'Analyse balancier par schema ORB'

        cv2.namedWindow(self.window_name)
        self.rect_sel = RectSelector(self.window_name, self.on_rect)
        
        self.list_centers = []


    def on_rect(self, rect):
        self.tracker.clear()
        self.tracker.add_target(self.frame, rect)

    def run(self):
        ''' Exécution de l'analyse vidéo, d'abord en mode pas à pas pour sélectionner un schéma de référence,
            puis en effectuant un matching entre les points clés détectés par ORB entre l'image courante et le schéma de référence '''
        
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
                self.paused = True  # pause forcée si aucun schéma de référence est sélectionné
                
            tracked = self.tracker.track(self.frame)
            draw_keypoints(vis, self.tracker.frame_points)

            # récupération des infos pour balancier lorsqu'on est en analyse et qu'on match
            if playing and len(tracked) > 0:
                tracked = tracked[0]
                cv2.polylines(vis, [np.int32(tracked.quad)], True, (255, 255, 255), 2)
                
                sumXY = [0, 0]
                
                for (x0, y0), (x1, y1) in zip(np.int32(tracked.p0), np.int32(tracked.p1)):
                    cv2.line(vis, (x0+w, y0), (x1, y1), (0, 255, 0))
                    
                    sumXY[0] += x1
                    sumXY[1] += y1
                    
                length = len(tracked.p1)
                mean = (sumXY[0] / length, sumXY[1] / length)
                
                timestamp = self.cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
            
                # information du pt courant
                center_data = CenterData(timestamp, mean[0], mean[1])
                self.list_centers.append(center_data)
                                
            self.rect_sel.draw(vis)
            cv2.imshow(self.window_name, vis)
            ch = cv2.waitKey(1)
            
            if ch == ord(' '):
                self.paused = not self.paused
            if ch == 27:
                break
            
        # analyse balancier des données
        return Balancier(self.list_centers).analyze()

if __name__ == '__main__':
    pass

