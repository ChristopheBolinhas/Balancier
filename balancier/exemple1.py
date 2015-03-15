'''
Created on 2 mars 2015

@author: mathieu.rosser
'''

# http://stackoverflow.com/questions/20259025/module-object-has-no-attribute-drawmatches-opencv-python

import cv2
from find_obj import filter_matches,explore_match

def manage_frame(img1, img2):
    # Initiate SIFT detector
    orb = cv2.SIFT()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)
    
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)#, crossCheck=True)
    
    matches = bf.knnMatch(des1, trainDescriptors = des2, k = 2)
    p1, p2, kp_pairs = filter_matches(kp1, kp2, matches)
    try:
        explore_match('find_obj', img1,img2,kp_pairs)#cv2 shows image
    except:
        pass

img1 = cv2.imread('NewTerrain.png',0)          # queryImage
img2 = cv2.imread('selectivePanorama.jpg',0)     # trainImage

cap = cv2.VideoCapture("../video/balancier_motifComplexe.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    
    if frame is None:
        break
    
    img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    manage_frame(img2, img1)
    
    cv2.imshow('frame', img1)
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

    
cv2.waitKey()
cv2.destroyAllWindows()
