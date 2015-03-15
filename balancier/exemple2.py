'''
Created on 2 mars 2015

@author: mathieu.rosser
'''

# https://gist.github.com/kattern/355d9b27fc29cd195310

import numpy as np
import cv2
from matplotlib import pyplot as plt
from find_obj import filter_matches,explore_match

 
# this code is taken from the opencv feature matching examples at
# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_matcher/py_matcher.html#matcher
# i swapped out the images
# note that i had to comment out the graphical output below as i received the error detailed in this post
# http://stackoverflow.com/questions/20172953/opencv-python-no-drawmatchesknn-function
 
# img1 is the queryImage
# img2 is the trainImage
 
#img1 = cv2.imread('01-IMG_0491.jpg',0)
#img1 = cv2.imread('02-IMG_0492.jpg',0)
#img1 = cv2.imread('03-IMG_0493.jpg',0)
#img1 = cv2.imread('04-IMG_0494.jpg',0)
img1 = cv2.imread('NewTerrain.png',0)
#img1 = cv2.imread('07-IMG_0497.jpg',0)
#img1 = cv2.imread('08-IMG_0498.jpg',0)
#img1 = cv2.imread('10-IMG_0500.jpg',0)
 
img2 = cv2.imread('NewPatternFixed.png',0)
#img2 = cv2.imread('rect_template.jpg',0)
#img2 = cv2.imread('star_template.jpg',0)
 
def manage_frame(img1, img2):
    # Initiate SIFT detector
    sift = cv2.SIFT()
     
    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
     
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
     
    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = (255,0,0),
                       matchesMask = matchesMask,
                       flags = 0)
     
    # errors if the line below is not commented out
    #img3 = cv2.drawMatchesKnn(img1,kp1,img2,kp2,matches,None,**draw_params)
    #img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10], flags=2)
     
    # what is the best way to quantify the how strong the match is?
    count_matches = 0
    for i in range(len(matches)):
        if matchesMask[i] == [1,0]:
            count_matches += 1
    print count_matches
     
    p1, p2, kp_pairs = filter_matches(kp1, kp2, matches)
    try:
        explore_match('find_obj', img1,img2,kp_pairs)#cv2 shows image
    except:
        pass


cap = cv2.VideoCapture("../video/balancier2_cut.mp4")

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

 
#plt.imshow(img3,),plt.show()
