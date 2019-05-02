# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 15:10:05 2019

@author: milos
"""

from threading import Thread
import pandas as pd


class Detector(Thread):
    def __init__(self, queue, toll_count, vehicle_count):
        super(Detector, self).__init__()

        self.queue = queue
        self.isRunning = False
        self.toll_count = toll_count
        self.vehicle_count = vehicle_count
        self.anomalies = []
        self.passes = []

    def run(self):
        print("Detector: Start!");
        self.isRunning = True
        while self.isRunning: #or not self.queue.empty():
            if not self.queue.empty():
                new_pass = self.queue.get()
                self.queue.task_done()
                self.passes.append(new_pass)
                #self.static_rules(new_pass)
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
                
        print("Detector: End!");
        print("======Statistics======")
        print("Total Passes: %s" % (len(self.passes)))
        print("Total Anomalies: %s" % (len(self.anomalies)))
        print("Percentage: %s" % ((len(self.anomalies)/len(self.passes))*100.))
        
        
        
        
    # def static_rules(self, new_pass):
    #     if (new_pass.toll.position in ('in', 'out') and new_pass.toll.capacity<self.vehicle_count/self.toll_count and new_pass.vehicle.type in ('bus','truck')):
    #         new_pass.anomaly='Smuggling/Trafficing'
    #     if (new_pass.toll.position in ('mid') and new_pass.speed>190 and new_pass.vehicle.luxury in ('yes') and new_pass.vehicle.type in ('car')):
    #          new_pass.anomaly='Kidnapping/Robbery'
    #     if (new_pass.toll.position in ('out') and new_pass.speed>190 and new_pass.vehicle.luxury in ('yes') and new_pass.vehicle.type in ('car')):
    #          new_pass.anomaly='Car Hijacking'
    #
    #     if (new_pass.anomaly!=None):
    #         self.anomalies.append(new_pass)
    #         print ('%s - Plate No %s' % (new_pass.anomaly, new_pass.vehicle.plate))

    def stop(self):
        self.isRunning = False

    def save(self):
        v = pd.DataFrame([x.to_dict() for x in self.passes])
        v.to_csv("../data/passes.csv", index=False)

        v = pd.DataFrame([x.to_dict() for x in self.anomalies])
        v.to_csv("../data/anomalies.csv", index=False)

