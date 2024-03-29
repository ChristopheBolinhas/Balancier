'''
Created on 7 mars 2015

@author: mathieu.rosser
'''

import numpy as np
import cv2
from matplotlib import pyplot as plt
from find_obj import filter_matches,explore_match


MIN_MATCH_COUNT = 10

img1 = cv2.imread('NewPatternFixed.png',0)          # queryImage
img2 = cv2.imread('box_in_scene.png',0) # trainImage

cv2.imshow("test", img2)

def manage_frame(img1, img2):
    # Initiate SIFT detector
    sift = cv2.SIFT()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    
    matches = flann.knnMatch(des1,des2,k=2)
    
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    
    if len(good)>MIN_MATCH_COUNT:
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()
    
        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,M)
    
        cv2.polylines(img2,[np.int32(dst)],True,255,3) #cv2.LINE_AA)
    
    else:
        print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
        matchesMask = None
    
    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)
    
    cv2.imshow("tests", img2)
    
    p1, p2, kp_pairs = filter_matches(kp1, kp2, matches)
    explore_match('find_obj', img1,img2,kp_pairs)#cv2 shows image
    
    #img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)
    
    #plt.imshow(img3, 'gray'),plt.show()

cap = cv2.VideoCapture("../video/balancier2_cut.mp4")

while cap.isOpened():
    ret, frame = cap.read()
    
    if frame is None:
        break
    
    img2 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    manage_frame(img1, img2)
    
    cv2.waitKey()
    
    cv2.imshow('frame', img1)
    
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cv2.waitKey()
cv2.destroyAllWindows()
