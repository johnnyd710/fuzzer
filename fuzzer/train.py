#!/usr/bin/python3.5
'''
created on: Feb 4th 2019
author: John DiMatteo
description: 

trains the clustering algorithm on offline data

in: offline data directory (directory)
out: centroids of kmeans centroids.txt

'''

from classifiers.kmeans import Kmeans
from classifiers.kmeans_dba import KmeansDBA
from offline import Offline
import numpy as np
import os

K=5 # no. of clusters
DATA_IN="out/traces" # location of training dataset
CENTROIDS_OUT="out/centroids" # location to put centroids after training
ALGORITHM="kmeans" # kmeans or dba?


def pad(s, m, fillval=0.0):
    """ pads with zeros so they are all equal length """
    lens = np.array([len(item) for item in s])
    mask = lens[:, None] > np.arange(lens.max())
    out = np.full(mask.shape, fillval)
    out[mask] = np.concatenate(s)
    return out


def load(path):
    max_length = 0
    signals = []
    for filename in os.listdir(path):
        filename = path + '/' + filename
        signals.append(np.load(filename))
    signals = pad(signals, max_length)
    print("%d signals loaded from %s" % (len(signals), path)) 
    return signals


def train():

    data = load(DATA_IN)

    data = np.vstack(data)
    print("Size of training data (rows, cols) ", data.shape)

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
    train()
    exit()
