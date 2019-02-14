import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

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

timeSeries = get_signals()

clus = np.genfromtxt('out.csv', delimiter=',', skip_header=True)

timeSeries = pd.DataFrame(data = timeSeries)
# check the results
s = pd.Series(clus[1:20,1])
clusters = s.unique()

for c in clusters:
    cluster_indeces = s[s==c].index
    print("Cluster %d number of entries %d" % (c, len(cluster_indeces)))
    timeSeries.T.iloc[:,cluster_indeces].plot()
    plt.show()