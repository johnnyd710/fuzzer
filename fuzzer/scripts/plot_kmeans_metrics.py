#!/usr/bin/python3.5
# pylint: disable=no-value-for-parameter
'''
created on: Dec. 19th 2018
author: John DiMatteo
description: 

returns a plot of f1 score as k is varied on the dataset

parameters:
--k_range -k range of k (1 to what?)
--dataset -d dataset to train on (the rest are used for testing)
--out -o location where to save file
'''

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('../')
import click
from state_detector import ts_cluster
from offline import Offline
import numpy as np
import test_harness
import train
import plot_centroids
import matplotlib.pyplot as plt
plt.style.use("ggplot")

# get response (offline for now)
msgs = ['reg0-bar', 'reg0-alt', 'reg0-bar-active', 'reg0-alt-active',
        'reg1-bar', 'reg1-alt', 'reg1-bar-active', 'reg1-alt-active']


@click.command()
@click.option('--k_range', '-k', default=10, help='range of k (1 to what?)')
@click.option('--out', '-o', default='./plot.png', help='Output for plot. default is ./plot.png.')
@click.option('--dataset', '-d', help='dataset to train on (the rest are used for testing)')
@click.option('--algorithm', '-a', help='which algorithm to use? kmeans or dba?')
def main(k_range, out, dataset, algorithm):

    tmp='./tmp'
    stats = np.zeros((2,k_range))
    for i in range(1, (k_range+1)):
        # initialize
        train.train(k=i,data_in=dataset,centroids_out=tmp, algorithm= algorithm)
        #plot_centroids.centroids(path=tmp)
        stats[0,(i-1)], stats[1, (i-1)] = test_harness.test(k=i,centroids_in=tmp, test_dir='./data', write=True)
    
    plt.figure(figsize=(15,10))
    plt.plot(stats[0]*100)
    plt.ylabel("Classification Accuracy (%)")
    plt.xlabel("K")
    plt.ylim(0, 100)
    plt.savefig("./accuracy.png")
    plt.close()

    plt.figure(figsize=(15,10))
    plt.plot(stats[1])
    plt.ylabel("Classification Entropy")
    plt.xlabel("K")
    plt.savefig("./entropy.png")
    

if __name__ == "__main__":
    main()
    exit()
