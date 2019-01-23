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

@click.command()
@click.option('--epsilon', '-e', default=100, help='epsilon value for similarity metric. default is 10000')
def main(epsilon):
    # initialize
    Detector = State_Detector(eps=epsilon)
    Offline_ = Offline()
    # determine which message to send

    # send the message

    # get response (offline for now)
    msgs = ['reg0-bar', 'reg0-alt', 'reg0-bar-active', 'reg0-alt-active',
            'reg1-bar', 'reg1-alt', 'reg0-bar-active', 'reg1-alt-active']

    for msg in range(10):
        msg = np.random.choice(msgs)
        click.echo(msg)
        response = Offline_.get_signal(msg)
        # process response 
        Detector.classify(msg, response)

if __name__ == "__main__":
    main()
    exit()