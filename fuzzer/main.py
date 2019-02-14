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

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import click
from classifiers.kmeans import Kmeans
from offline import Offline
import numpy as np

from tslearn.utils import to_time_series_dataset

# get response (offline for now)
msgs = ['reg0-bar', 'reg0-alt', 'reg0-bar-active', 'reg0-alt-active',
        'reg1-bar', 'reg1-alt', 'reg0-bar-active', 'reg1-alt-active']


@click.command()
@click.option('--k', '-k', default=4, help='K, number of clusters for K-Means. default is 3.')
@click.option('--txt_out', '-o', default='./out', help='Output directory for logging/stats. default is ./out.')
@click.option('--centroids_in', '-i', default='./out/centroids', help='Input directory for centroids. default is ./out/centroids.')
def main(k, txt_out, centroids_in):
    # initialize
    Detector = Kmeans(k)
    Offline_ = Offline()

    Kmeans.load_centroids(centroids_in)
    print("Centroids successfully loaded from %s" % centroids_in)

    # determine which message to send
    #for m in msgs:
    #    Offline_.load(m)

    Offline_.load('mpl-test')

    #data = to_time_series_dataset(Offline_.signals)
    data = np.array(Offline_.signals)
    print(data.shape)

    for msg in range(5):
        msg = np.random.choice(msgs)
        click.echo(msg)
        response = Offline_.get_signal(msg)
        # process response 
        # classify
        
if __name__ == "__main__":
    main()
    exit()