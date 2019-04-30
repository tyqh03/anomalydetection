# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 19:35:18 2019

@author: milos
"""
import pandas as pd 
from sklearn.ensemble import IsolationForest
import numpy as np 
import tensorly as tl
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split



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


train, test = train_test_split(fdata, test_size=0.2)

print(test.shape)

# training the model
clf = IsolationForest()
clf.fit(train)

# predictions
pred_train = clf.predict(train)
pred_test = clf.predict(test)



print(len(test))
print(len([n for n in pred_test if n == -1]))