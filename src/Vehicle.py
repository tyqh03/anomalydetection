# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 12:17:49 2019

@author: milos
"""

import uuid
from numpy import random


class Vehicle:
    def __init__(self, model, v_type, luxury, tolls):
        self.plate = uuid.uuid4()
        self.model = model
        self.v_type = v_type
        self.luxury = luxury

        self.toll = tolls[random.choice(range(0, len(tolls)))]
        self.reroute(tolls)

        if self.distance > 1:
            self.distance = random.randint(1, self.distance)

    def reroute(self, tolls):
        if self.toll.t_type == "net":
            new_toll_index = random.choice(range(0, len(self.toll.balance)), p=self.toll.balance)
            self.distance = self.toll.distance[new_toll_index]
            self.toll = tolls[new_toll_index]
        else:
            new_toll_index = random.choice(range(0, len(tolls)))
            self.toll = tolls[new_toll_index]
            self.distance = 1

    def drive(self):
        self.distance -= 1
        return self.distance == 0

    def __repr__(self):
        return "%s;%s;%s;%s" % (self.plate, self.model, self.v_type, self.luxury)
    
    def to_dict(self):
        return {
            'plate': self.plate,
            'model': self.model,
            'v_type': self.v_type,
            'luxury': self.luxury,
        }
