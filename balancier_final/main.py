#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Application de calcul de mouvements de balancier
@author: christophe.bolinhas, mathieu.rosser
'''

import sys
from appcircles import AppCircles
from appmotif import AppMotif
from appschema import AppSchema
from balancier import BalancierDataViewer


if __name__ == '__main__':
    print __doc__

    enum_code = "motif_complexe"
    
    if len(sys.argv) > 1:
        enum_code = sys.argv[1]
        
    show_video = True
    
    if(show_video):
        print("Affichage : ON")
    else:
        print("Affichage : OFF")
    
    # 375 pixels ---> 0.50 mètres
    RATIO_PIXEL_PER_METER = 375.0 / 0.50
    PENDULUM_LENGTH = 0.60

    balancier_analyze = None
    
    if enum_code == "circle_blue":
        balancier_analyze = AppCircles("../video/balancier_cercleB.mp4", "B", show_video).run()
    
    elif enum_code == "circle_red":
        balancier_analyze = AppCircles("../video/balancier_cercleR.mp4", "R", show_video).run()
    
    elif enum_code == "circle_green":
        balancier_analyze = AppCircles("../video/balancier_cercleG.mp4", "G", show_video).run()
    
    elif enum_code == "circle_rgb":
        balancier_analyze = AppCircles("../video/balancier_cercleRGB.mp4", "B", show_video).run()
    
    elif enum_code == "schema1":
        balancier_analyze = AppSchema("../video/balancier_schema1.mp4").run()
    
    elif enum_code == "schema2":
        balancier_analyze = AppSchema("../video/balancier_schema2.mp4").run()
    
    elif enum_code == "motif_complexe":
        balancier_analyze = AppMotif("../video/balancier_motif.mp4", "../balancier/selectivePanorama.jpg", show_video).run()
    
    if balancier_analyze is not None:
        BalancierDataViewer(balancier_analyze).view_data(PENDULUM_LENGTH, RATIO_PIXEL_PER_METER)

