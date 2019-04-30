# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 19:48:45 2019

@author: milos
"""

# Load the Pandas libraries with alias 'pd' 
import pandas as pd 
from sklearn.metrics import f1_score
import numpy as np 
import seaborn as sns
from scipy.stats import multivariate_normal
import matplotlib.pyplot as plt

def feature_normalize(dataset):
    mu = np.mean(dataset, axis=0)
    sigma = np.std(dataset, axis=0)
    return (dataset - mu) / sigma

#probabilities, isAnomaly
def select_threshold(probs, test_data):
    best_epsilon = 0
    best_f1 = 0
    f = 0
    stepsize = (max(probs) - min(probs)) / 1000;
    epsilons = np.arange(min(probs), max(probs), stepsize)
    for epsilon in np.nditer(epsilons):
        predictions = (probs < epsilon)
        f = f1_score(test_data, predictions, average='binary')
        if f > best_f1:
            best_f1 = f
            best_epsilon = epsilon

    return best_f1, best_epsilon



data = pd.read_csv("../data/gauss.csv") 

toll_dist=data.groupby(["toll_name"]).size().to_frame("size")
toll_dist["size"].plot(kind='hist')
plt.show()

X=toll_dist["size"].values

X_normalized=feature_normalize(X)

sns.distplot(X);
#sns.distplot(X_normalized);

m=X_normalized.mean()
std=X_normalized.std()
test_data=[1,0,0,1,0]

print(m)
print(std)
print(X_normalized)

p=multivariate_normal.pdf(X_normalized, mean=m, cov=std)
f1, e=select_threshold(p, test_data)


print(f1)
print(e)
print(p)

outliers = np.asarray(np.where(p < e))
print(outliers)