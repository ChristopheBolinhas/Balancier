#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Application de calcul de mouvements de balancier
Analyse de vidéo de balancier avec détection de motifs SIFT
Basé sur https://gist.github.com/kattern/355d9b27fc29cd195310
@author: christophe.bolinhas, mathieu.rosser
'''

import cv2
from find_obj import filter_matches, explore_match
from balancier import Balancier, CenterData
 
class AppMotif():
    ''' Classe d'analyse de vidéo basé sur un motif et détection de points-clés SIFT pour correspondances entre image et motif,
        soit en détectant les extremums en X (gauche, droite), soit en se basant sur le nombre maximum de correspondances '''
    
    def __init__(self, src_video, src_motif, show_video = True):
        self.img_motif = cv2.imread(src_motif, 0)
        self.show_video = show_video
        
        self.cap = cv2.VideoCapture(src_video)
        self.frame = None
        
        self.list_centers = []
        
        # Initiate SIFT detector
        self.sift = cv2.SIFT()
        
        self.kpMotif, self.descMotif = self.sift.detectAndCompute(self.img_motif,None)
            
    def run(self, threshold_nb_points = 0):
        ''' exécution de l'analyse vidéo, soit par extremums, soit par nombre de correspondances avec seuil de maximum '''
        
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            
            if frame is None:
                break
            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.manage_frame(frame)
                        
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break
        
        cv2.destroyAllWindows()
        
        # analyse balancier
        return Balancier(self.list_centers).analyze(threshold_nb_points)

 
    def manage_frame(self, image):         
        ''' analyse d'une image pour correspondance SIFT entre l'image et le motif '''
        
        # find the keypoints and descriptors with SIFT
        kp1, des1 = self.kpMotif, self.descMotif
        kp2, des2 = self.sift.detectAndCompute(image,None)
         
        # FLANN parameters
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
         
        search_params = dict(checks=50)   # or pass empty dictionary
         
        flann = cv2.FlannBasedMatcher(index_params,search_params)
         
        matches = flann.knnMatch(des1,des2,k=2)
         
        # Need to draw only good matches, so create a mask
        matchesMask = [[0,0] for i in xrange(len(matches))]
         
        # ratio test as per Lowe's paper
        for i,(m,n) in enumerate(matches):
            if m.distance < 0.7*n.distance:
                matchesMask[i]=[1,0]
                  
        # what is the best way to quantify the how strong the match is?
        count_matches = 0
        for i in range(len(matches)):
            if matchesMask[i] == [1,0]:
                count_matches += 1
                         
        p1, p2, kp_pairs = filter_matches(kp1, kp2, matches)
        
        try:
            explore_match('Analyse balancier par motif Sift', self.img_motif, image, kp_pairs)
            
            mean = [0, 0]
        
            for x, y in p2:
                mean[0] += x
                mean[1] += y
                
            mean = [m / len(p2) for m in mean]
            
            timestamp = self.cap.get(cv2.cv.CV_CAP_PROP_POS_MSEC)
            
            # données centre pour analyse balancier
            center_data = CenterData(timestamp, mean[0], mean[1], count_matches)
            self.list_centers.append(center_data)
            
        except:
            pass

if __name__ == '__main__':
    pass
