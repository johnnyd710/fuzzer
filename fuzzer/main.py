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
from state_detector import State_Detector
from offline import Offline
import numpy as np

from tslearn.utils import to_time_series_dataset

# get response (offline for now)
msgs = ['reg0-bar', 'reg0-alt', 'reg0-bar-active', 'reg0-alt-active',
        'reg1-bar', 'reg1-alt', 'reg0-bar-active', 'reg1-alt-active']


@click.command()
@click.option('--k', '-k', default=3, help='K, number of clusters for K-Means. default is 3.')
def main(k):
    # initialize
    Detector = State_Detector(k=k)
    Offline_ = Offline()

    # determine which message to send
    for m in msgs:
        Offline_.load(m)

    #data = to_time_series_dataset(Offline_.signals)
    data = np.array(Offline_.signals)
    print(data.shape)

    Detector.pretrain(data)

    Detector.plot()

    for msg in range(10):
        msg = np.random.choice(msgs)
        click.echo(msg)
        response = Offline_.get_signal(msg)
        # process response 
        Detector.classify(msg, response)

if __name__ == "__main__":
    main()
    exit()