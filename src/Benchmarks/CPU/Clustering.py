from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import pandas as pd
import numpy as np
import time


class Clustering:
    def __init__(self, clusters):
        self.clusters=clusters

    def getDistanceByPoint(self, data, model):
        distance = pd.Series()
        for i in range(0, len(data)):
            Xa = np.array(data.loc[i])
            Xb = model.cluster_centers_[model.labels_[i] - 1]
            distance.at[i] = np.linalg.norm(Xa - Xb)
        return distance

    def kmeans(self, data):
        min_max_scaler = preprocessing.StandardScaler()
        np_scaled = min_max_scaler.fit_transform(data)
        data = pd.DataFrame(np_scaled)

        # reduce to 2 importants features
        pca = PCA(n_components=2)
        data = pca.fit_transform(data)

        # standardize these 2 new features
        min_max_scaler = preprocessing.StandardScaler()
        np_scaled = min_max_scaler.fit_transform(data)
        data = pd.DataFrame(np_scaled)

        # calculate with different number of centroids to see the loss plot (elbow method)
        kmeans = KMeans(n_clusters=self.clusters).fit(data)
        scores = kmeans.score(data)
        kmeans.predict(data)

        outliers_fraction = 0.01
        # get the distance between each point and its nearest centroid. The biggest distances are considered as anomaly
        distance = self.getDistanceByPoint(data, kmeans)
        number_of_outliers = int(outliers_fraction * len(distance))
        threshold = distance.nlargest(number_of_outliers).min()

    def evaluate(self, data):
        start = time.time()

        self.kmeans(data)

        end = time.time()
        return end - start
