# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 12:17:59 2019

@author: milos
"""

import uuid


class Toll:
    def __init__(self, t_type, position, balance, distance):
        self.name = uuid.uuid4()
        self.t_type = t_type
        self.position = position
        self.balance = balance
        self.distance = distance

        if t_type == "checkpoint":
            self.balance = []
            self.distance = []

    def __repr__(self):
        return "%s;%s;%s;%s;%s" % (self.name, self.t_type, self.position)
        
    def to_dict(self):
        return {
            'name': self.name,
            't_type': self.t_type,
            'position': self.position
        }
