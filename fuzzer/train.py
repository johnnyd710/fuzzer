#!/usr/bin/python3.5
# pylint: disable=no-value-for-parameter
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

import click
from state_detector import ts_cluster
from offline import Offline
import numpy as np
import os

from tslearn.utils import to_time_series_dataset

# get response (offline for now)
msgs = ['reg0-bar', 'reg0-alt', 'reg0-bar-active', 'reg0-alt-active',
        'reg1-bar', 'reg1-alt', 'reg0-bar-active', 'reg1-alt-active']


@click.command()
@click.option('--k', '-k', default=4, help='K, number of clusters for K-Means. default is 3.')
@click.option('--data_in', '-d', help='Location of training dataset.')
@click.option('--centroids_out', '-o', default='./out/centroids', help='Output directory for centroids. default is ./out/centroids.')
@click.option('--algorithm', '-a', default='kmeans', help='Clustering algorithm to use. default is kmeans, options are (kmeans, dba).')
def main(k, data_in, centroids_out, algorithm):
    # initialize
    Detector = ts_cluster(k)
    Offline_ = Offline()

    Offline_.load(data_in)

    #data = to_time_series_dataset(Offline_.signals)
    data = np.array(Offline_.signals)
    print("Size of training data (rows, cols) = (%d, %d)" % (data.shape[0], data.shape[1]))

    if algorithm.lower() == 'kmeans':
        Detector.k_means_clust(data, 10, 100)
    elif algorithm.lower() == 'dba':
        Detector.k_means_clust_dba(data, 10, 100)
    else:
        print("Improper argument specified. kmeans or dba!")
        exit()


    Detector.save_centroids(centroids_out)

if __name__ == "__main__":
    main()
    exit()