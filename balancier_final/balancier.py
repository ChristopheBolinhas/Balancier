#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Application de calcul de mouvements de balancier
Classes permettant d'analyser les mouvements de balancier et d'obtenir des résultats mathématiques
@author: christophe.bolinhas, mathieu.rosser
'''


import math

class CenterData():
    ''' Représente un centre détecté dans une image, à un certain temps, avec un certain nombre de pts de correspondances '''
    
    def __init__(self, timestamp, x, y, nb_points = 0):
        self.timestamp = timestamp
        self.x = x
        self.y = y
        self.nb_points = nb_points
        
    def __repr__(self):
        return "[%f] (%f,%f) - %f\n" %(self.timestamp, self.x, self.y, self.nb_points)
    
    
class BalancierData():
    ''' Représente un résultat d'analyse de balancier: période et distance, permettant de calculer l'angle, la hauteur max et la vitesse '''
    
    def __init__(self, periode, distance):
        self.periode = periode
        self.distance = distance
        
    def calculate_angle(self, L, ratio_pixel_per_meter):
        Lpixel = L * ratio_pixel_per_meter
        opp = self.distance / 2.0
        self.angle = math.degrees(math.asin(opp / Lpixel))
        return self.angle
        
    def calculate_maximum_height(self, L, ratio_pixel_per_meter):
        self.calculate_angle(L, ratio_pixel_per_meter)
        self.max_height = L - L * math.cos(math.radians(self.angle))
        return self.max_height
        
    def calculate_bottom_velocity(self, L, ratio_pixel_per_meter):
        self.calculate_angle(L, ratio_pixel_per_meter)
        self.bottom_velocity = math.sqrt(2 * 9.81 * L * (1 - math.cos(math.radians(self.angle))))
        return self.bottom_velocity
    
    @staticmethod
    def calculate_real_period(L):
        return 2.0 * math.pi * math.sqrt(L / 9.81)
    
    def __repr__(self):
        return "(%f [s], %f [°])" %(self.periode, self.distance)
    
    
class BalancierDataViewer():
    ''' Représente un visualisateur des résultats d'analyse de balancier, avec affichage tabulaire des mesures et calculs '''
    
    def __init__(self, list_balancier_data):
        self.list_balancier_data = list_balancier_data
        
    def view_data(self, L, ratio_pixel_per_meter):
        
        print("Analyse du mouvement de balancier pour L = %f [m] (ratio %f [px]/[m])" %(L, ratio_pixel_per_meter))
        print("Période théorique = %f [s]" %BalancierData.calculate_real_period(L))
        
        print("N° \t Période [ms] \t Largeur [px] \t Angle [°] \t Hauteur [m] \t Vitesse [m/s]")
        
        i = 1
        for b in self.list_balancier_data:
            angle = b.calculate_angle(L, ratio_pixel_per_meter)
            height = b.calculate_maximum_height(L, ratio_pixel_per_meter)
            velocity = b.calculate_bottom_velocity(L, ratio_pixel_per_meter)
            
            print("%d \t %f \t %f \t %f \t %f \t %f" %(i, b.periode, b.distance, angle, height, velocity))            
            
            i += 1

class Balancier():
    ''' Classe permettant d'analyse de balancier, à partir de liste de points de centres 
        Analyse effectuée par les extremums gauche et droite de balancement, 
        ou par l'identification des points où le nombre de correspondances est maxium '''
    
    COUNTER_MARGIN = 4
    
    def __init__(self, list_centers):
        self.list_centers = list_centers
        
    def analyze(self, threshold_nb_points = 0):
        return self.analyze_by_nb_points(threshold_nb_points) if threshold_nb_points > 0 else self.analyze_by_extremum()
    
    def analyze_by_extremum(self):
        ''' Analyse balancier en cherchant les extremum gauche (minimum X) et droite (maximum X), avec marge d'erreur de tolérance sous forme de décompteur '''
        
        is_looking_for_left = True
        list_right_center = []
        list_left_center = []
        const_counter = Balancier.COUNTER_MARGIN
        counter = const_counter
        current_max = None
        
        for center in self.list_centers:
            if is_looking_for_left:
                if current_max is None or current_max.x > center.x:
                    current_max = center
                    counter = const_counter
                else:
                    counter-=1
            else:
                if current_max is None or current_max.x < center.x:
                    current_max = center
                    counter = const_counter
                else:
                    counter-=1
                
            if counter == 0:
                if not is_looking_for_left:
                    list_right_center.append(current_max)
                
                elif len(list_right_center) > 0:
                    list_left_center.append(current_max)
                    
                is_looking_for_left = not is_looking_for_left
                
        
        list_balancier_data = []
        
        last_center = None
        it_list_left_center = iter(list_left_center)
        
        for centers_right in list_right_center:
            if last_center is not None:
                dt = abs(centers_right.timestamp - last_center.timestamp)
                dx = abs(centers_right.x - it_list_left_center.next().x)
                balancier_data = BalancierData(dt, dx)
                list_balancier_data.append(balancier_data)
                
            last_center = centers_right
        
        return list_balancier_data
    
    def analyze_by_nb_points(self, threshold_nb_points):
        ''' Analyse balancier en cherchant les points de max(correspondances), avec tolérance d'erreur sous forme de décompteur '''
        
        list_max_points = []
        list_local_max_points = []
        const_counter = Balancier.COUNTER_MARGIN
        counter = const_counter
        
        for center in self.list_centers:
            if center.nb_points > threshold_nb_points:
                list_local_max_points.append(center)
                counter = const_counter
            else:
                counter -= 1
                
            if len(list_local_max_points) > 0 and counter == 0:
                max_points = max(list_local_max_points, key=lambda x: x.nb_points)
                list_max_points.append(max_points)
                list_local_max_points = []
                
        
        list_balancier_data = []
                 
        for i in range(2, len(list_max_points), 3):
            current = list_max_points[i]
            previous_dt = list_max_points[i-2]
            previous_dx = list_max_points[i-1]
            
            dt = abs(current.timestamp - previous_dt.timestamp)
            dx = abs(current.x - previous_dx.x)
            balancier_data = BalancierData(dt, dx)
            list_balancier_data.append(balancier_data)
        
        return list_balancier_data


if __name__ == '__main__':
    pass
