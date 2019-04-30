# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 12:17:59 2019

@author: milos
"""

import uuid

class Toll:
    def __init__(self, type, position, capacity, balance, distance):
        self.id=uuid.uuid4()
        self.type = type
        self.position = position
        self.capacity = capacity
        self.balance = balance
        self.distance = distance
        
        
    def __repr__(self):
        return "%s;%s;%s;%s" % (self.id, self.type, self.position, self.capacity)
        
    def to_dict(self):
        return {
            'toll_name': self.id,
            'type': self.type,
            'position': self.position,
            'capacity': self.capacity,
        }