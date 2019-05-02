# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 12:42:22 2019

@author: milos
"""


from threading import Thread
import numpy as np
from numpy import random
from random import gauss
from datetime import timedelta
import pandas as pd
import time

from Vehicle import Vehicle
from Toll import Toll
from Map import Map
from Pass import Pass


class Simulator(Thread):
    def __init__(self,
                 queue,
                 toll_count, connectivity, distance,
                 vehicle_count, vehicle_model_dist, vehicle_type_dist, vehicle_luxury_dist,
                 toll_type_dist, toll_position_dist,
                 environment_datetime,
                 simulation_time):
        super(Simulator, self).__init__()

        self.passes = []
        self.elapsed = 0
        self.queue=queue
        self.environment_datetime = environment_datetime
        self.simulation_time = simulation_time

        self.__init_map__(toll_count, connectivity, distance)
        self.__init_tolls__(toll_count, toll_type_dist, toll_position_dist)
        self.__init_vehicles__(vehicle_count, vehicle_model_dist, vehicle_type_dist, vehicle_luxury_dist)

    def __init_map__(self, toll_count, connectivity, distance):
        self.map = Map(toll_count, connectivity, distance)

        v = pd.DataFrame(self.map.get_c())
        v.to_csv("../data/map_c.csv", index=True)
        v = pd.DataFrame(self.map.get_p())
        v.to_csv("../data/map_p.csv", index=True)
        v = pd.DataFrame(self.map.get_d())
        v.to_csv("../data/map_d.csv", index=True)
        
    def __init_tolls__(self, toll_count, toll_type_dist, toll_position_dist):
        self.tolls = []
        
        for i in range(toll_count):
            self.tolls.append(Toll(random.choice(list(toll_type_dist.keys()), p=list(toll_type_dist.values())),
                                   random.choice(list(toll_position_dist.keys()), p=list(toll_position_dist.values())),
                                   np.squeeze(np.asarray(self.map.get_p()[i])),
                                   np.squeeze(np.asarray(self.map.get_d()[i]))))

        v = pd.DataFrame([x.to_dict() for x in self.tolls])
        v.to_csv("../data/tolls.csv", index=False)

    def __init_vehicles__(self, vehicle_count, vehicle_model_dist, vehicle_type_dist, vehicle_luxury_dist):
        self.vehicles = []

        for i in range(vehicle_count):
            self.vehicles.append(Vehicle(random.choice(vehicle_model_dist),
                                         random.choice(list(vehicle_type_dist.keys()), p=list(vehicle_type_dist.values())),
                                         random.choice(list(vehicle_luxury_dist.keys()), p=list(vehicle_luxury_dist.values())),
                                         self.tolls))

        v = pd.DataFrame([x.to_dict() for x in self.vehicles])
        v.to_csv("../data/vehicles.csv", index=False)

    def new_pass(self, vehicle):
        speed = gauss(120, 20)
        p = Pass(vehicle, vehicle.toll, speed, self.environment_datetime + timedelta(hours=self.elapsed))
        self.passes.append(p)
        self.queue.put(p)

    def run(self):
        print("Simulation: Start!")

        while self.elapsed < self.simulation_time:
            start_time = time.time()
            count = 0
            for i in range(len(self.vehicles)):
                v = self.vehicles[i]
                if v.drive():
                    self.new_pass(v)
                    v.reroute(self.tolls)
                    count += 1

            print("%s - %s passes" % (self.environment_datetime + timedelta(hours=self.elapsed), count))

            sleep = 1-(time.time() - start_time)
            if sleep > 0:
                time.sleep(sleep)

            self.elapsed += 1
        print("Simulation: End!")
        print("Duration: %sh" % self.simulation_time)
