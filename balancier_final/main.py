#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 14 mars 2015

@author: christophe.bolinhas, mathieu.rosser
'''


import numpy as np
import cv2
from appcircles import AppCircles
    

if __name__ == '__main__':
    print __doc__

    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0
        
    color = "B"
    show_video = True
	enum_code = "circles"
    print("Application de calcul de mouvement de balancier")
	
	if(show_video):
		print("Affichage : ON")
	else
		print("Affichage : OFF")
		
	
		
		
	switch(enum_code)
    AppCircles(video_src, color, show_video).run()

