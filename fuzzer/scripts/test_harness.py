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

# get response (offline for now)
msgs = ['reg0-bar', 'reg0-alt', 'reg0-bar-active', 'reg0-alt-active',
        'reg1-bar', 'reg1-alt', 'reg0-bar-active', 'reg1-alt-active']

@click.command()
@click.option('--k', '-k', default=4, help='K, number of clusters for K-Means. default is 3.')
@click.option('--txt_out', '-o', default='./out.csv', help='Output file for logging/stats. default is "./out/out.csv".')
@click.option('--centroids_in', '-i', default='./out/centroids', help='Input directory for centroids. default is "./out/centroids".')
@click.option('--test_dir', '-t', default='./data', help='Directory to test on. default is "./data".')
def main(k, txt_out, centroids_in, test_dir):
    # initialize
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
    out = open(txt_out, "wb")
    pickle.dump(stats, out)
    out.close()
    
    print("writing completed")

    print(stats)

        
if __name__ == "__main__":
    main()
    exit()