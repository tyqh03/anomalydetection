# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 12:42:22 2019

@author: milos
"""


from threading import Thread
import numpy as np
from numpy import random
from random import gauss
from datetime import datetime, timedelta
import time

from Vehicle import Vehicle
from Toll import Toll
from Map import Map
from Pass import Pass

import settings



class Simulator(Thread):
    def __init__(self, 
                 toll_count, connectivity, distance,
                 vehicle_count,vehicle_model_dist, vehicle_type_dist, vehicle_luxury_dist, 
                 toll_type_dist, toll_position_dist,
                 environment_datetime,
                 duration
                 ):
        super(Simulator, self).__init__()
        self.__init_map__(toll_count, connectivity, distance)
        self.__init_tolls__(toll_count, vehicle_count, toll_type_dist, toll_position_dist)
        self.__init_vehicles__(toll_count, vehicle_count, vehicle_model_dist, vehicle_type_dist, vehicle_luxury_dist)
        self.passes=[]
        self.environment_datetime=environment_datetime
        self.hours=0
        self.isRunning=False
        self.duration=duration

    def __init_map__(self, toll_count, connectivity, distance):
        self.map=Map(toll_count, connectivity, distance)
        
    def __init_tolls__(self, toll_count, vehicle_count, toll_type_dist, toll_position_dist):
        capacity_array=random.random(toll_count)
        capacity_array=capacity_array*vehicle_count/capacity_array.sum()
        self.tolls=[]
        
        for i in range(toll_count):
            self.tolls.append(Toll(random.choice( list(toll_type_dist.keys()) ,p=list(toll_type_dist.values())), random.choice(list(toll_position_dist.keys()),p=list(toll_position_dist.values())), capacity_array[i], np.squeeze(np.asarray(self.map.get_p()[i])), np.squeeze(np.asarray(self.map.get_d()[i]))))
            
    
    def __init_vehicles__(self,toll_count, vehicle_count, vehicle_model_dist, vehicle_type_dist, vehicle_luxury_dist):
        self.vehicles=[]
        for i in range(vehicle_count):
            start_toll=self.tolls[random.randint(0,toll_count)]
            toll_index=random.choice(range(0, len(start_toll.balance)),p=start_toll.balance)
            next_toll=self.tolls[toll_index]
            to_distance=random.randint(1,start_toll.distance[toll_index])
            
            v=Vehicle(random.choice(vehicle_model_dist),random.choice(list(vehicle_type_dist.keys()),p=list(vehicle_type_dist.values())), random.choice(list(vehicle_luxury_dist.keys()),p=list(vehicle_luxury_dist.values())), next_toll, to_distance)
            self.vehicles.append(v)
    
    def new_pass(self,vehicle):
        #print("Vehicle %s passed toll %s" % (vehicle, vehicle.next_toll));
        start_toll=vehicle.next_toll
        toll_index=random.choice(range(0, len(start_toll.balance)),p=start_toll.balance)
        vehicle.next_toll=self.tolls[toll_index]
        vehicle.to_distance=start_toll.distance[toll_index]
        p=Pass(vehicle, start_toll, gauss(130, 50),self.environment_datetime+ timedelta(hours=self.hours))
        self.passes.append(p)
        return p
        
        
    def run(self):
        self.isRunning=True
        print("Simulation - Start!");
        while self.isRunning:
            for i in range(len(self.vehicles)):
                if(self.vehicles[i].drive()):
                    p=self.new_pass(self.vehicles[i])
                    settings.queue.put(p)
            #time.sleep(1)
            self.hours+=1
            if (self.hours==self.duration):
                self.isRunning=False
        
        print("Simulation - End!");
