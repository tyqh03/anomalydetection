from sklearn.datasets.samples_generator import make_blobs
import numpy as np

from Clustering import Clustering
from Classification import Classification
from MultivariateGauss import MultivariateGauss
from TensorDecomposition import TensorDecomposition

import warnings
warnings.filterwarnings('ignore')

class CPUImpl:
    def __init__(self, size, features):
        self.size = size
        self.features = features

        self.test_data, t = make_blobs(n_samples=self.size, n_features=self.features)
        self.test_tensor_data = np.random.random((self.size, self.features, self.features))

        self.kmeans = Clustering(10)
        self.svm = Classification()
        self.gauss = MultivariateGauss()
        self.tensor = TensorDecomposition()


    def evaluate(self):
        print("Data set: %s samples" % self.size)
        print("Features: %s" % self.features)
        print("======")
        print("KMeans: %s s" % self.kmeans.evaluate(self.test_data))
        print("OneClassSVM: %s s" % self.svm.evaluate(self.test_data, "svm"))
        print("Gauss: %s s" % self.gauss.evaluate(self.test_data))
        print("Parafac: %s s" % self.tensor.evaluate(self.test_tensor_data))




cpuTest = CPUImpl(1000, 10)
cpuTest.evaluate()

