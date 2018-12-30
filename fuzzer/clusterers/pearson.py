from cluster import Cluster
import numpy as np
from scipy.cluster.hierarchy import fcluster
import scipy.cluster.hierarchy as hac
from scipy.stats import pearsonr
import time

class Pearson(Cluster):
    def __init__(self, name, data):
        self.data = data
        super().__init__(name)

    def r(self, x, y):
        r = pearsonr(x,y)[0]
        return 1 - r

    def add_data(self, new_data):
        self.data = np.concatenate((self.data, new_data), axis=0)

    def peek(self, n=3):
        print(self.data[0:n,:])

    def plot_clusters(self):
        import matplotlib.pyplot as plt
        import pandas as pd

        timeSeries = pd.DataFrame(data = self.data)

        # check the results
        s = pd.Series(self.clus)
        clusters = s.unique()

        for c in clusters:
            cluster_indices = s[s==c].index
            print("Cluster %d number of entries %d" % (c, len(cluster_indices)))
            timeSeries.T.iloc[:,cluster_indices].plot(figsize=(20,15))
            plt.savefig('figs/' + self.name + '-clus' + str(c) + '.png')

    def cluster(self, k=2):
        """ k is the number of clusters you'd like to extract """

        print("Clustering responses...")
        start = time.time()
        Z = hac.linkage(self.data,  method='single', metric=self.r)
        print("Time taken:", time.time() - start)
        print("classifying...")
        self.clus = fcluster(Z, k, criterion='maxclust')
        print("done.")


