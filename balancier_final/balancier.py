#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 14 mars 2015

@author: christophe.bolinhas, mathieu.rosser
'''


import math

class CenterData():
    
    def __init__(self, timestamp, x, y):
        self.timestamp = timestamp
        self.x = x
        self.y = y
        
    def __repr__(self):
        return "[%f] (%f,%f)\n" %(self.timestamp, self.x, self.y)
    
class BalancierData():
    
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
    
    def __init__(self, list_centers):
        self.list_centers = list_centers
        
    def analyze(self):
        is_looking_for_left = True
        list_right_center = []
        list_left_center = []
        const_counter = 4
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

if __name__ == '__main__':
    pass
