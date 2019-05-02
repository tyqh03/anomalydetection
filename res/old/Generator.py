import numpy as np
from numpy import random
import uuid


class Vehicle:
    def __init__(self, plate, type, brand_new):
        self.plate = plate
        self.type = type
        self.brand_new = brand_new
        
    def __str__(self):
        return "%s;%s;%s" % (self.plate, self.type, self.brand_new)
    
    def __repr__(self):
        return "%s;%s;%s" % (self.plate, self.type, self.brand_new)
    
    def to_dict(self):
        return {
            'plate': self.plate,
            'v_type': self.type,
            'brand_new': self.brand_new,
        }
    
class Toll:
    def __init__(self, id, type, position, capacity, balance):
        self.id=id
        self.type = type
        self.position = position
        self.capacity = capacity
        self.balance = balance
        
        
    def __str__(self):
        return "%s;%s;%s;%s" % (self.id, self.type, self.position, self.capacity)
    
    def __repr__(self):
        return "%s;%s;%s;%s" % (self.id, self.type, self.position, self.capacity)
        
    def to_dict(self):
        return {
            'id': self.id,
            't_type': self.type,
            'position': self.position,
            'capacity': self.capacity,
        }
        
class Map:
    def __init__(self, tolls_count, connectivity):
        self.G= nx.erdos_renyi_graph(tolls_count,connectivity) 
        while not nx.is_connected(self.G):
            self.G= nx.erdos_renyi_graph(tolls_count,connectivity)
        self.matrix= nx.to_numpy_matrix(self.G)
        self.matrix_p=self.matrix
        
        traversed=np.zeros(tolls_count)
        while True:
            min_n_sum=0
            min_p_sum=0
            min_i=0
            for k in range(np.argmax(traversed==0),tolls_count):
                temp_arr=np.squeeze(np.asarray(self.matrix_p[k]))
                local_n_sum=sum(i for i in temp_arr if i < 0)
                local_p_sum=sum(i for i in temp_arr if i > 0)
                if local_n_sum<min_n_sum:
                    min_n_sum=local_n_sum
                    min_p_sum=local_p_sum
                    min_i=k
                    
            traversed[min_i]=1
            min_n_sum=abs(min_n_sum)
            if min_n_sum==0:
                break;
            p=random.random(int(min_n_sum))
            p=p*(1-min_p_sum)/p.sum()
            
            self.matrix_p[min_i,:][self.matrix_p[min_i,:]==-1]=p
        

    def get_net(self):
        return self.matrix
    
    def get_p(self):
        return self.matrix_p
    
class Pass:
    def __init__(self, vehicle, toll, speed, timestamp, time_of_day):
        self.vehicle=vehicle
        self.toll=toll
        self.speed=speed
        self.timestamp=timestamp
        self.time_of_day=time_of_day
        
         
    def to_dict(self):
        return {
            **self.vehicle.to_dict()
            ,**{
            'speed': self.speed,
            'timestamp': self.timestamp,
            'time_of_day': self.time_of_day
            },
            **self.toll.to_dict()
        }
        
class Generator:
    def __init__(self, vehicles_count, tolls_count):
        self.vehicles_count=vehicles_count
        self.tolls_count=tolls_count
        
    def create_vehicles(self,type_dist, brand_new_dist):
        vehicle_type = ['car','bus','truck']
        brand_new = ['yes','no']
        self.vehicles=[]
        for i in range(self.vehicles_count):
            self.vehicles.append(Vehicle(uuid.uuid4(), random.choice(vehicle_type,p=[type_dist['car'], type_dist['bus'], type_dist['truck']]), random.choice(brand_new,p=[brand_new_dist['yes'], brand_new_dist['no']])))
       
    def create_map(self, connectivity):
        self.map=Map(self.tolls_count,connectivity)
        
    def create_tolls(self, type_dist, position_dist, probability_dist):
        toll_type = ['checkpoint','net']
        position = ['in','mid', 'out']
        capacity_array=random.random(self.tolls_count)
        capacity_array=capacity_array*self.vehicles_count/capacity_array.sum()
        self.tolls=[]
        for i in range(self.tolls_count):
            self.tolls.append(Toll(uuid.uuid4(), random.choice(toll_type,p=[type_dist['checkpoint'], type_dist['net']]), random.choice(position,p=[position_dist['in'], position_dist['mid'], position_dist['out']]), capacity_array[i], probability_dist[i]))
       
    def create_passes(self):
        self.passes=[]
        for i in range(self.vehicles_count):
            self.passes.append(Pass(self.vehicles[i],self.tolls[random.choice(len(self.tolls))], random.randint(80,220), uuid.uuid4(), random.choice(['day','night'])))
    

import pandas as pd 
import networkx as nx

def main():
    generator=Generator(1000,5)
    generator.create_map(0.5)
    generator.create_vehicles({'car': 0.6, 'bus': 0.2, 'truck':0.2},{'yes': 0.4, 'no': 0.6})
    generator.create_tolls({'checkpoint': 0.4, 'net': 0.6},{'in': 0.1, 'out': 0.1, 'mid':0.8}, generator.map.matrix_p)
    generator.create_passes()
    
   
    
    v = pd.DataFrame([x.to_dict() for x in generator.passes])
    v.to_csv("passes.csv", index=False)
     

if __name__== "__main__":
  main()