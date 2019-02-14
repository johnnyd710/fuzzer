#!/usr/bin/python3.5
# pylint: disable=no-value-for-parameter
'''
created on: Dec. 19th 2018
author: John DiMatteo
description: 

smart algorithm to determine the validity of msgs in i2c protocol.

steps:
determine which message to send (Input Generator)
send the message (Message Sender)
analyze response (Change Detector)

'''
import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('../')
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import click
from state_detector import ts_cluster
from offline import Offline
import numpy as np
import csv
import pickle
from tslearn.utils import to_time_series_dataset
from collections import Counter
from sklearn.metrics import f1_score
import math

# get response (offline for now)
msgs = ['reg0-bar', 'reg0-alt', 'reg0-bar-active', 'reg0-alt-active',
        'reg1-bar', 'reg1-alt', 'reg1-bar-active', 'reg1-alt-active']

def consistency(data):
    """ data is a list, return % of highest count """
    value, total = 0, 0
    for key in data:
        value += Counter(data[key]).most_common(1)[0][1] # get count of value with highest frequency
        total += len(data[key])

    return  (value / total)

def eta(data, unit='natural'):
    base = {
        'shannon' : 2.,
        'natural' : math.exp(1),
        'hartley' : 10.
    }
    if len(data) <= 1:
        return 0

    counts = Counter()

    for d in data:
        counts[d] += 1

    ent = 0

    probs = [float(c) / len(data) for c in counts.values()]
    for p in probs:
        if p > 0.:
            ent -= p * math.log(p, base[unit])

    return ent

@click.command()
@click.option('--k', '-k', default=4, help='K, number of clusters for K-Means. default is 3.')
@click.option('--centroids_in', '-i', default='../out/centroids', help='Input directory for centroids. default is "../out/centroids".')
@click.option('--test_dir', '-t', default='./data', help='Directory to test on. default is "./data".')
@click.option('--write', '-w', default=True, help='Write new stats file? Default True.')
def main(k, centroids_in, test_dir, write):
    test(k, centroids_in, test_dir, write)

def test(k, centroids_in, test_dir, write):
    stats_file = './out.pkl'
    # initialize
    print(write)
    if write==1:
        Detector = ts_cluster(k)
        Offline_ = Offline()

        stats = {key:[] for key in msgs}

        Detector.load_centroids(centroids_in)
        print("Centroids successfully loaded from %s" % centroids_in)

        # determine which message to send
        for m in msgs:
                responses = Offline_.load_msg(m)
                for response in responses:
                        stats[m].append(Detector.classify(response))

        # save to pickle file
        out = open(stats_file, "wb")
        pickle.dump(stats, out)
        out.close()
        
        print("writing completed")

    else:
        file = open(stats_file,'rb')
        stats = pickle.load(file)
        file.close()

    all_vals = []
    for l in list(stats.values()):
        all_vals += l

    entropy = eta(all_vals)
    error_rate = consistency(stats)

    print(error_rate, entropy)
    return error_rate, entropy

        
if __name__ == "__main__":
    main()
    exit()
