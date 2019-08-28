from sklearn.metrics import f1_score
from scipy.stats import multivariate_normal

import numpy as np
import time


class MultivariateGauss:
    def __init__(self):
        pass

    def feature_normalize(self, dataset):
        mu = np.mean(dataset, axis=0)
        sigma = np.std(dataset, axis=0)
        return (dataset - mu) / sigma

    # probabilities, isAnomaly
    def select_threshold(self, probs, test_data):
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

    def gauss(self, data):
        for i in range(len(data[0])):
            X=[row[i] for row in data]
            X_normalized = self.feature_normalize(X)

            m = X_normalized.mean()
            std = X_normalized.std()
            test_data = np.random.choice([0, 1], size=len(data), p=[.9, .1])
            #print(test_data)
            p = multivariate_normal.pdf(X_normalized, mean=m, cov=std)
            f1, e = self.select_threshold(p, test_data)

            outliers = np.asarray(np.where(p < e))

    def evaluate(self, data):
        start = time.time()

        self.gauss(data)

        end = time.time()
        return end - start
