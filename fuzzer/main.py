#!/usr/bin/python3.5
# pylint: disable=no-value-for-parameter
'''
created on: Dec. 19th 2018
author: John DiMatteo
description: 

smart algorithm to determine the validity of msgs in i2c protocol.
unlocks proprietary access to registers

'''

import click
import random
from fuzzer import Fuzzer
#from cluster import cluster
#from I2C import...
from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
import sys
import numpy as np
sys.path.insert(0, './protocols')
sys.path.insert(0, '../tests')
from fuzzer_tests import get_signals
from fastdtw import fastdtw

MIN_LENGTH = 26707

def dtw(x, y):
    distance, path = fastdtw(x, y, dist=1)
    return distance

@click.command()
@click.option('--epsilon', '-e', default=10000, help='epsilon value for DBSCAN clustering. default is 10000')
def main(epsilon):

    # initiate each register in every address as inactive
    #TODO : implement this is as a class?
    registers = {i:'inactive' for i in range(256)}
    i2c_dict = {i:registers for i in range(256)}

    Fuzz = Fuzzer(MIN_LENGTH)

    while True:
        # send msgs
        #for adr in i2c_dict:
        #    for reg in i2c_dict[adr]:
        #        send_msg()

        # get msgs
        data = get_signals('../Scripts/Applications/Data_processing/signals', 5)
        
        i=0
        for signal in data:
            # add (signal, (adr,reg))
            Fuzz.add(signal, 'adr,reg'+str(i))
            i+=1

        data = get_signals('../Scripts/Applications/Data_processing/signals-2', 5)

        for signal in data:
            # add (signal, (adr,reg))
            Fuzz.add(signal, 'adr,reg'+str(i))
            i+=1
        
        # process data
        clus = DBSCAN(eps = epsilon, min_samples=2, metric = dtw).fit(Fuzz.data)
        click.echo(clus.labels_)

        # get active msgs
        # if label is one, change label in Fuzz to active

        for msg, info in Fuzz.msg_dict.items():
            info['membership'] = clus.labels_[info['data']]

        #plot expected active and inactive msgs
        for i in np.unique(clus.labels_):
            Fuzz.plot_all_signals(i)

        exit()


    # output grammar

    # pass active msgs to cnn

    # train cnn

    # output results

    exit()

if __name__ == "__main__":
    main()