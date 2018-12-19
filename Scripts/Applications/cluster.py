'''
created on Nov-4-2018
author: john dimatteo
jdimatteo@uwaterloo.ca

fuzzer.py <directory of signals>

- recieves signals and outputs clusters
'''
import numpy as np
import os
import sys
import csv
import time

from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

import scipy.cluster.hierarchy as hac
from scipy.cluster.hierarchy import fcluster

from scipy import stats

def r(x, y):
    r = stats.pearsonr(x, y)[0]
    return 1 - r # correlation to distance: range 0 to 2

def dtw(x, y):
    distance, path = fastdtw(x, y, dist=1)
    return distance

def get_signals():
    '''
    gets signals from specified directory 
    and returns a (n, l, 1) numpy array
    where n is number of distinct signals and
    l is length of each signal.
    '''
    directory = sys.argv[1]

    list_of_signals = []

    n = 0
    for filename in os.listdir(directory):
        filename = directory + '/' + filename
        list_of_signals.append(np.genfromtxt(filename, delimiter=','))
        n+=1
    
    min_l = 1e10
    for s in list_of_signals:
        l = len(s)
        if l < min_l: min_l = l

    signals = np.zeros([n, min_l])   #, 1])

    for i, arr in enumerate(list_of_signals):
        arr = arr[0:min_l]
        signals[i] = arr #.reshape(l,1)

    print(len(signals[0]))
    return signals
    
def plot(Z):
    import matplotlib.pyplot as plt
    # Plot dendogram
    plt.figure(figsize=(25, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    hac.dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
    )
    plt.show()

def clusters(timeSeries, Z, k, plot=False):
    import matplotlib.pyplot as plt
    import pandas as pd
    # k Number of clusters I'd like to extract
    results = fcluster(Z, k, criterion='maxclust')

    timeSeries = pd.DataFrame(data = timeSeries)

    # check the results
    s = pd.Series(results)
    clusters = s.unique()

    for c in clusters:
        cluster_indeces = s[s==c].index
        print("Cluster %d number of entries %d" % (c, len(cluster_indeces)))
        if plot:
            timeSeries.T.iloc[:,cluster_indeces].plot()
            plt.show()

    return results

if __name__ == '__main__':
    print("Clustering responses...")
    start = time.time()

    data = get_signals()
    #print(clf(data))

    # Do the clustering    
    Z = hac.linkage(data,  method='single', metric=dtw)
    print("Time taken:", time.time() - start)
    #plot(Z)
    clus = clusters(data, Z, 6, plot=True)

    outname = sys.argv[2]

    with open(outname + '.csv', 'w') as fh:
        writer = csv.writer(fh, delimiter=',')
        writer.writerow(['id','val'])
        writer.writerows(enumerate(clus))

    exit()