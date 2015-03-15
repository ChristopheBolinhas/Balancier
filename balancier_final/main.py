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
        
    color = "R"
    show_video = True
    
    AppCircles(video_src, color, show_video).run()

