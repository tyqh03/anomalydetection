# -*- coding: utf-8 -*-
"""
Created on Sat Apr 27 12:22:17 2019

@author: milos
"""

import networkx as nx
import numpy as np
from numpy import random
from copy import deepcopy


class Map:
    def __init__(self, toll_count, connectivity, distance):
        self.G = nx.erdos_renyi_graph(toll_count, connectivity)

        while not nx.is_connected(self.G):
            self.G = nx.erdos_renyi_graph(toll_count, connectivity)
        self.matrix_c = nx.to_numpy_matrix(self.G)

        for (u, v, w) in self.G.edges(data=True):
            w['weight'] = random.randint(0, 10)
        
        self.__init_properties__(toll_count, distance)
        
    def __init_properties__(self, toll_count, distance):
        self.matrix_p = deepcopy(self.matrix_c)
        self.matrix_d = deepcopy(self.matrix_c)
        
        self.matrix_p[self.matrix_p == 1] = -1
        self.matrix_d[self.matrix_d == 1] = -1

        traversed = np.zeros(toll_count)
        
        while True:
            min_n_sum = 0
            min_p_sum = 0
            min_i = 0
            for k in range(np.argmax(traversed == 0), toll_count):
                temp_arr = np.squeeze(np.asarray(self.matrix_p[k]))
                local_n_sum = sum(i for i in temp_arr if i < 0)
                local_p_sum = sum(i for i in temp_arr if i > 0)
                if local_n_sum < min_n_sum:
                    min_n_sum = local_n_sum
                    min_p_sum = local_p_sum
                    min_i = k

            traversed[min_i] = 1
            min_n_sum = abs(min_n_sum)
            if min_n_sum == 0:
                break
            p = random.random(int(min_n_sum))
            p = p*(1-min_p_sum)/p.sum()
            
            self.matrix_p[min_i, :][self.matrix_p[min_i, :] == -1] = p
            
            d = random.choice(list(distance), int(min_n_sum))
            self.matrix_d[min_i, :][self.matrix_d[min_i, :] == -1.] = d

        for i in range(toll_count):
            for j in range(i):
                self.matrix_d[j, i] = self.matrix_d[i, j]

    def get_c(self):
        return self.matrix_c
    
    def get_p(self):
        return self.matrix_p
    
    def get_d(self):
        return self.matrix_d


