import tensorly as tl
from tensorly.decomposition import parafac

import pandas as pd
import numpy as np
import time


class TensorDecomposition:
    def __init__(self):
        pass

    def parafac(self, data):
        t=tl.tensor(data)
        factors = parafac(t, rank=1)

    def evaluate(self, data):
        start = time.time()

        self.parafac(data)

        end = time.time()
        return end - start
