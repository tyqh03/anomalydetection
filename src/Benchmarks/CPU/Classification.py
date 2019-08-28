from sklearn import preprocessing

from sklearn.svm import OneClassSVM
from sklearn.ensemble import IsolationForest

import pandas as pd
import numpy as np
import time


class Classification:
    def __init__(self):
        pass

    def classification_svm(self, data):
        min_max_scaler = preprocessing.StandardScaler()
        np_scaled = min_max_scaler.fit_transform(data)
        data = pd.DataFrame(np_scaled)

        outliers_fraction = 0.01
        model = OneClassSVM(nu=0.95 * outliers_fraction)  # nu=0.95 * outliers_fraction  + 0.05
        data = pd.DataFrame(np_scaled)
        model.fit(data)
        model.predict(data)

    def classification_tree(self, data):
        clf = IsolationForest()
        clf.fit(data)
        pred_train = clf.predict(data)

    def evaluate(self, data, type):
        if type=="svm":
            start = time.time()

            self.classification_svm(data)

            end = time.time()
            return end - start
        else:
            start = time.time()

            self.classification_tree(data)

            end = time.time()
            return end - start
