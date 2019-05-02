
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def visualize_data(data):
    fig, axs = plt.subplots(ncols=2)


    sns.countplot(x = 'v_type',
                  data = data,
                  order = data['v_type'].value_counts().index, ax=axs[0])
    
    
    sns.countplot(x = 'brand_new',
                  data = data,
                  order = data['brand_new'].value_counts().index, ax=axs[1])
    
    
    fig.show()
    
    fig, axs = plt.subplots(ncols=3)
    
    
    sns.countplot(x = 't_type',
                  data = data,
                  order = data['t_type'].value_counts().index, ax=axs[0])
    
    
    sns.countplot(x = 'position',
                  data = data,
                  order = data['position'].value_counts().index, ax=axs[1])
    
    
    sns.distplot(data['capacity']);
    fig.show()
    
    
    fig, axs = plt.subplots(ncols=2)
    
    
    
    sns.countplot(x = 'time_of_day',
                  data = data,
                  order = data['time_of_day'].value_counts().index, ax=axs[0])
    
    sns.distplot(data['speed']);
    
    fig.show()


rdata = pd.read_csv("passes.csv")

#print(rdata.info())
#print(rdata.head())

#visualize_data(rdata)

v_type_map=pd.Series(range(len(rdata["v_type"].unique())),index=rdata["v_type"].unique()).to_dict()
brand_new_map=pd.Series(range(len(rdata["brand_new"].unique())),index=rdata["brand_new"].unique()).to_dict()
t_type_map=pd.Series(range(len(rdata["t_type"].unique())),index=rdata["t_type"].unique()).to_dict()
position_map=pd.Series(range(len(rdata["position"].unique())),index=rdata["position"].unique()).to_dict()
time_of_day_map=pd.Series(range(len(rdata["time_of_day"].unique())),index=rdata["time_of_day"].unique()).to_dict()



anomalies=rdata.loc[(rdata['position'] =='out') & (rdata['v_type'] =='truck') & (rdata['capacity'] =='truck')]
print(anomalies)

fdata=pd.DataFrame()
fdata["v_type"]=rdata["v_type"].map(v_type_map)
fdata["brand_new"]=rdata["brand_new"].map(brand_new_map)
fdata["t_type"]=rdata["t_type"].map(t_type_map)
fdata["position"]=rdata["position"].map(position_map)
fdata["time_of_day"]=rdata["time_of_day"].map(time_of_day_map)
fdata["speed"]=rdata["speed"]
fdata["capacity"]=rdata["capacity"]

#print(fdata)



#print(fdata.shape)
#print(fdata["speed"].mean())
#print(fdata["speed"].std())


#==============================================================================
# X=fdata[["speed","capacity"]].values
# # split into train and test
# # split into train and test
# X_train = X[:50]
# X_test = X[50:]
# 
# # density estimation
# mu = 1/X_train.shape[0] * np.sum(X_train, axis=0) 
# sigma_squared = 1/X_train.shape[0] * np.sum((X_train - mu) ** 2, axis=0)
# 
# # probability calculation for test
# def p(x, mu, sigma_squared):
#     return np.prod(1 / np.sqrt(2*np.pi*sigma_squared) * np.exp(-(x-mu)**2/(2*sigma_squared)), axis=1)
# 
# p_test = p(X_test, mu, sigma_squared)
# 
# # visualization using contour plot
# delta = 5
# x = np.arange(0, 300, delta)
# y = np.arange(0, 300, delta)
# x, y = np.meshgrid(x, y)
# z = p(np.hstack((x.reshape(-1, 1), y.reshape(-1, 1))), mu, sigma_squared).reshape(x.shape)
# 
# plt.figure(figsize=(10, 10))
# CS = plt.contour(x, y, z)
# plt.clabel(CS, inline=1, fontsize=12)
# plt.scatter(X[:50, 0], X[:50, 1], c='b', alpha=0.7)
# plt.scatter(X[50:, 0], X[50:, 1], c='r', alpha=0.7)
# 
#==============================================================================

# looking at the plot setting epsilon around p=0.003 seems like a fair value.

#plt.scatter(fdata['speed'], fdata['capacity'], marker = "x")

#X=fdata[["v_type","brand_new","t_type","position","time_of_day","speed","capacity"]].values
X=fdata



#==============================================================================
# from sklearn.decomposition import FactorAnalysis, PCA
# import tensortools as tt
# from tensortools.operations import unfold as tt_unfold, khatri_rao
# import tensorly as tl
# from tensorly import unfold as tl_unfold
# from tensorly.decomposition import parafac
#==============================================================================

# import some useful functions (they are available in utils.py)
#from utils import *

# import some useful functions (they are available in utils.py)
#from utils import *
# Perform CP decompositon using TensorLy

#print(X)
# Perform CP decompositon using TensorLy
#factors_tl = parafac(X, rank=7)

#import Tkinter
#top = Tkinter.Tk()
# Code to add widgets will go here...
#top.mainloop()

# Perform CP decomposition using tensortools
#U = tt.cp_als(X, rank=7, verbose=False)
#factors_tt = U.factors.factors

# Reconstruct M, with the result of each library
#M_tl = tt.reconstruct(factors_tl)
#M_tt = tt.reconstruct(factors_tt)
#print(factors_tl)
# plot the decomposed factors
#tt.plot_factors(factors_tl)
#tt.plot_factors(factors_tt)

       
#==============================================================================
# from sklearn.preprocessing import StandardScaler
# scaler=StandardScaler()#instantiate
# scaler.fit(X) # compute the mean and standard which will be used in the next command
# X_scaled=scaler.transform(X)# fit and transform can be applied together and I leave that for simple exercise
# # we can check the minimum and maximum of the scaled features which we expect to be 0 and 1
# print ("after scaling minimum %s" % (X_scaled.min(axis=0)))
# 
# from sklearn.decomposition import PCA
# pca=PCA(n_components=2) 
# pca.fit(X_scaled) 
# X_pca=pca.transform(X_scaled) 
# #let's check the shape of X_pca array
# print ("shape of X_pca", X_pca.shape)
# import numpy as np
# ex_variance=np.var(X_pca,axis=0)
# ex_variance_ratio = ex_variance/np.sum(ex_variance)
# print (ex_variance_ratio)
# 
# from sklearn.decomposition import PCA
# import pylab as pl
# pl.scatter(X_pca,X_pca,c='r',marker='s')
# 
#==============================================================================
#==============================================================================
# import matplotlib.pyplot as plt
# from sklearn.cluster import KMeans
# kmeans = KMeans(n_clusters=3).fit(fdata)
# centroids = kmeans.cluster_centers_
# print(centroids)
#==============================================================================
