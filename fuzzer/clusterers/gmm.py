from cluster import Cluster
import numpy as np
import time
from sklearn.mixture import GaussianMixture
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute
import pandas as pd

class GMM(Cluster):
    def __init__(self, name, data):
        self.data = data
        self.features = self.make_features(data)
        self.model = GaussianMixture(n_components=2)
        super().__init__(name)

    def add_data(self, new_data):
        features = self.make_features(new_data)
        self.features = np.concatenate((self.features, features), axis=0)

    def peek(self, n=3):
        print(self.features[0:n,:])

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
        self.model.fit(self.features)
        print("Time taken:", time.time() - start)
        print("classifying...")
        self.clus = self.model.predict(self.features)
        print("done.")

    def make_features(self, d):
        """ create time series features describing the signal . takes a long time for large signals """
        d = pd.DataFrame(data = d)
        d = d.stack()
        d.index.rename([ 'id', 'time' ], inplace = True )
        d = d.reset_index()
        features = extract_features(d[d['id'] == 1][1:1000], column_id='id', column_sort = "time", impute_function=impute)
        return features
