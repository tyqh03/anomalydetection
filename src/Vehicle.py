# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 12:17:49 2019

@author: milos
"""

import uuid
from numpy import random
from Toll import Toll

class Vehicle:
    def __init__(self, model, type, luxury, next_toll, to_distance):
        self.plate=uuid.uuid4()
        self.model=model
        self.type = type
        self.luxury = luxury
        
        self.next_toll=next_toll
        self.to_distance=to_distance
        
    def drive(self):
        self.to_distance-=1
        return self.to_distance==0
            
        
    def __repr__(self):
        return "%s;%s;%s;%s" % (self.plate, self.model, self.type, self.luxury)
    
    def to_dict(self):
        return {
            'plate': self.plate,
            'model': self.model,
            'type': self.type,
            'luxury': self.luxury,
        }