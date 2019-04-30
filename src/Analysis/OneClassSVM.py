# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 09:45:45 2019

@author: milos
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 09:31:01 2019

@author: milos
"""
import pandas as pd
import numpy as np

import matplotlib
import seaborn
import matplotlib.dates as md
from matplotlib import pyplot as plt

from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.covariance import EllipticEnvelope
#from pyemma import msm # not available on Kaggle Kernel
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM





rdata = pd.read_csv("../data.csv") 


model_map=pd.Series(range(len(rdata["model"].unique())),index=rdata["model"].unique()).to_dict()
luxury_map=pd.Series(range(len(rdata["luxury"].unique())),index=rdata["luxury"].unique()).to_dict()
type_map=pd.Series(range(len(rdata["type"].unique())),index=rdata["type"].unique()).to_dict()
position_map=pd.Series(range(len(rdata["position"].unique())),index=rdata["position"].unique()).to_dict()



fdata=pd.DataFrame()
fdata["model"]=rdata["model"].map(model_map)
fdata["luxury"]=rdata["luxury"].map(luxury_map)
fdata["type"]=rdata["type"].map(type_map)
fdata["position"]=rdata["position"].map(position_map)
fdata["speed"]=rdata["speed"]
fdata["capacity"]=rdata["capacity"]

data=fdata

min_max_scaler = preprocessing.StandardScaler()
np_scaled = min_max_scaler.fit_transform(data)
data = pd.DataFrame(np_scaled)

outliers_fraction=0.01
model =  OneClassSVM(nu=0.95 * outliers_fraction) #nu=0.95 * outliers_fraction  + 0.05
data = pd.DataFrame(np_scaled)
model.fit(data)
# add the data to the main  
print(pd.DataFrame(model.predict(data)).value_counts())