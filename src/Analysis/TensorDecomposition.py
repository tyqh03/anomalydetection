# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 10:49:25 2019

@author: milos
"""

import pandas as pd 
import numpy as np 
import tensorly as tl
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from tensorly.decomposition import parafac

rdata = pd.read_csv("../data.csv") 
#926b738c-fea4-4bce-bdfc-881bf1444f3a
#81673e77-d246-415b-9e57-ac9d5e0f9dbc


plates=(rdata["plate"].unique())[:100]
tolls=rdata["toll_name"].unique()#[:3]
timestamps=rdata["timestamp"].unique()#[:3]



m_tensor=[]
for l in range(len(timestamps)):
    m_matrix=[]
    current_timestamp=timestamps[l]
    temp_data=rdata[rdata["timestamp"]==current_timestamp]
    for v in range(len(plates)):
        m_row=[]
        current_plate=plates[v]
        for t in range(len(tolls)):
            current_toll=tolls[t]
            p=float(temp_data[(temp_data["plate"]==current_plate) & (temp_data["toll_name"]==current_toll)].shape[0])
            m_row.append(p)
        m_matrix.append(m_row)
    m_tensor.append(m_matrix)
    

#print(m_tensor)
    

X=tl.tensor(m_tensor)

factors = parafac(X, rank=1)


#print(factors[0])



#print(len(factors))
# =============================================================================
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# plt.scatter(factors[:,0], factors[:,1], factors[:,2], c='r', marker='o')
# 
# =============================================================================



fig, ax = plt.subplots(3)

y=factors[0]
x = np.arange(len(y))
ax[0].plot(x,y, 'b')


y=factors[1]
x = np.arange(len(y))
ax[1].plot(x,y, 'b')


y=factors[2]
x = np.arange(len(y))
ax[2].plot(x,y, 'b')


fig.show()

