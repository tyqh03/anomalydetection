# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 15:10:05 2019

@author: milos
"""

from threading import Thread
import time
import random
from datetime import datetime, timedelta
import pandas as pd


import settings
from Simulator import Simulator


class Detector(Thread):
    def __init__(self, toll_count, vehicle_count):
        super(Detector, self).__init__()
        self.isRunning=False
        self.toll_count=toll_count
        self.vehicle_count=vehicle_count
        self.anomalies=[]
        self.data=[]
        
    def run(self):
        print("Detector - Start!");
        self.isRunning=True
        while self.isRunning==True:
            if (settings.queue.empty()==False):
                new_pass = settings.queue.get()
                settings.queue.task_done()
                self.data.append(new_pass)
                self.static_rules(new_pass)
            #else:
# =============================================================================
#                 df=pd.DataFrame([x.to_dict() for x in self.data])
#                 leftSide=df.groupby(["toll_name"]).size().to_frame('size')
#                 temp = df.drop_duplicates(subset='toll_name', inplace=False)
#                 rightSide=temp[['toll_name','capacity']]
#                 dfinal=pd.merge(leftSide, rightSide, on='toll_name', how='left')
#                 
#                 if (dfinal[dfinal['size'] > dfinal['capacity']].shape[0]>0):
#                     print(dfinal[dfinal['size'] > dfinal['capacity']].iloc[0])
# =============================================================================
                    #print("Higher capacity than usual - Toll: %s" %())
        self.save()
                
        print("Detector - End!");
        print ("======Statistics======")
        print ("Total Passes: %s" % (len(self.data)))
        print ("Total Anomalies: %s" % (len(self.anomalies)))
        print ("Percentage: %s" % ((len(self.anomalies)/len(self.data))*100.))
        
        
        
        
    def static_rules(self, new_pass):
        if (new_pass.toll.position in ('in', 'out') and new_pass.toll.capacity<self.vehicle_count/self.toll_count and new_pass.vehicle.type in ('bus','truck')):
            new_pass.anomaly='Smuggling/Trafficing'
        if (new_pass.toll.position in ('mid') and new_pass.speed>190 and new_pass.vehicle.luxury in ('yes') and new_pass.vehicle.type in ('car')):
             new_pass.anomaly='Kidnapping/Robbery'
        if (new_pass.toll.position in ('out') and new_pass.speed>190 and new_pass.vehicle.luxury in ('yes') and new_pass.vehicle.type in ('car')):
             new_pass.anomaly='Car Hijacking'
             
        if (new_pass.anomaly!=None):
            self.anomalies.append(new_pass)
            print ('%s - Plate No %s' % (new_pass.anomaly, new_pass.vehicle.plate))
            
    def save(self):
        v = pd.DataFrame([x.to_dict() for x in self.data])
        v.to_csv("data.csv", index=False)
        

def main():
    duration = 168
    toll_count = 20
    connectivity = 0.2
    distance = range(10,20)
    vehicle_count=1000
    vehicle_model_dist=['BMW','Audi','Fiat','Mercedes-Benz','Chrysler','Nissan','Volvo','Mazda','Mitsubishi','Ferrari','Alfa Romeo','Toyota','Maybach','Porsche','Hyundai','Honda','Suzuki','Ford','Cadillac','Kia','Bentley','Chevrolet','Dodge','Lamborghini','Lincoln','Subaru','Volkswagen','Spyker', 'Rolls-Royce','Maserati','Lexus','Aston Martin','Land Rover','Tesla','Bugatti',]
    vehicle_type_dist={'car': 0.6, 'bus': 0.2, 'truck':0.2}
    vehicle_luxury_dist={'yes': 0.4, 'no': 0.6}
    toll_type_dist={'checkpoint': 0.4, 'net': 0.6}
    toll_position_dist={'in': 0.1, 'out': 0.1, 'mid':0.8}
    environment_datetime=datetime.now()
    
    settings.init()

    sim=Simulator(toll_count,connectivity,distance,
                  vehicle_count,vehicle_model_dist, vehicle_type_dist, vehicle_luxury_dist,
                  toll_type_dist, toll_position_dist,
                  environment_datetime,
                  duration)
    
    detector=Detector(toll_count, vehicle_count)
   
    sim.start()
    detector.start()
    sim.join()
    detector.isRunning=False
    

     

if __name__== "__main__":
  main()