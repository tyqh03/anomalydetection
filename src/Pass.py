# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 12:40:40 2019

@author: milos
"""


class Pass:
    def __init__(self, vehicle, toll, speed, timestamp):
        self.vehicle = vehicle
        self.toll = toll
        self.speed = speed
        self.timestamp = timestamp

        self.Anomaly = None

    def to_dict(self):
        return {
            **self.vehicle.to_dict(),
            **self.toll.to_dict(),
            **{
                'speed': self.speed,
                'timestamp': self.timestamp
            },
        }
