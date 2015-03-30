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

    # code de la démo à lancer
    enum_code = "circle_blue"
    
    if len(sys.argv) > 1:
        enum_code = sys.argv[1]
        
    SHOW_VIDEO = True
    
    # seuil de nombre de correspondances trouvées entre motif et image courante
    THRESHOLD_NB_MATCHES = 20
    # correspondance entre image et monde réel: 375 pixels ---> 0.50 mètres
    RATIO_PIXEL_PER_METER = 375.0 / 0.50
    # longueur pendule en mètre
    PENDULUM_LENGTH = 0.60

    if SHOW_VIDEO:
        print("Affichage : ON")
    else:
        print("Affichage : OFF")
    
    balancier_analyze = None
    
    # lancement de l'analyse des vidéos
    if enum_code == "circle_blue":
        print("Exemple avec split couleur bleue, threshold, ouverture et les cercles de Hough")
        balancier_analyze = AppCircles("../video/balancier_cercleB.mp4", "B", SHOW_VIDEO).run()
    
    elif enum_code == "circle_red":
        print("Exemple avec split couleur rouge, threshold, ouverture et les cercles de Hough")
        balancier_analyze = AppCircles("../video/balancier_cercleR.mp4", "R", SHOW_VIDEO).run()
    
    elif enum_code == "circle_green":
        print("Exemple avec split couleur verte, threshold, ouverture et les cercles de Hough")
        balancier_analyze = AppCircles("../video/balancier_cercleG.mp4", "G", SHOW_VIDEO).run()
    
    elif enum_code == "circle_rgb":
        print("Exemple avec split couleur RGB, threshold, ouverture et les cercles de Hough")
        balancier_analyze = AppCircles("../video/balancier_cercleRGB.mp4", "B", SHOW_VIDEO).run()
    
    elif enum_code == "schema1":
        print("Exemple avec détection de schéma simple, algorithme : Orb")
        balancier_analyze = AppSchema("../video/balancier_schema1.mp4").run()
    
    elif enum_code == "schema2":
        print("Exemple avec détection de schéma simple, algorithme : Orb")
        balancier_analyze = AppSchema("../video/balancier_schema2.mp4").run()
    
    elif enum_code == "motif_extremum":
        print("Exemple avec détection de motif complexe par extremum, algorithme : Sift")
        balancier_analyze = AppMotif("../video/balancier_motif.mp4", "../balancier/selectivePanorama.jpg", SHOW_VIDEO).run()
        
    elif enum_code == "motif_match":
        print("Exemple avec détection de motif complexe par nombre de correspondances, algorithme : Sift")
        balancier_analyze = AppMotif("../video/balancier_motif.mp4", "../video/selectivePanorama.jpg", SHOW_VIDEO).run(THRESHOLD_NB_MATCHES)
    
    # affichage des résultats
    if balancier_analyze is not None:
        BalancierDataViewer(balancier_analyze).view_data(PENDULUM_LENGTH, RATIO_PIXEL_PER_METER)

