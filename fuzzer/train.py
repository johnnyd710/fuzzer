#!/usr/bin/python3.5
'''
created on: Feb 4th 2019
author: John DiMatteo
description: 

trains the clustering algorithm on offline data

in: offline data directory (directory)
out: centroids of kmeans centroids.txt

'''

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from classifiers.kmeans import Kmeans
from classifiers.kmeans_dba import KmeansDBA
from offline import Offline
import numpy as np
import os

K=5 # no. of clusters
DATA_IN="out/traces" # location of training dataset
CENTROIDS_OUT="out/centroids" # location to put centroids after training
ALGORITHM="kmeans" # kmeans or dba?
def main():
    train()

def train():
    # initialize
    Offline_ = Offline()

    Offline_.load(DATA_IN)

    #data = to_time_series_dataset(Offline_.signals)
    data = np.array(Offline_.signals)
    print("Size of training data (rows, cols) = (%d, %d)" % (data.shape[0], data.shape[1]))

    if ALGORITHM.lower() == 'kmeans':
        Detector = Kmeans(K)
    elif ALGORITHM.lower() == 'dba':
        Detector = KmeansDBA(K)
    else:
        print("Improper argument specified. kmeans or dba!")
        exit()

    Detector.k_means_clust(data, 10, 100)
    Detector.save_centroids(CENTROIDS_OUT)

if __name__ == "__main__":
    main()
    exit()
