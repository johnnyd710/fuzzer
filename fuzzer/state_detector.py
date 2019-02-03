#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
created on: Jan. 19th 2019
author: John DiMatteo
description: 
-- transform system response (a time series signal) into a finite string representation accepted by the Input Generator (or the Learner)

data:
-- previous responses from the system

psuedocode:

'''
from fastdtw import fastdtw
import numpy as np
import matplotlib.pyplot as plt

from tslearn.clustering import TimeSeriesKMeans

from ts_cluster import ts_cluster

def dtw(x, y):
    distance, path = fastdtw(x, y, dist=1)
    return distance

class State_Detector:
    
    def __init__(self, k):
        """ signals is a list of tuples : [(msg,response, label)]"""
        self.signals = []
        #self.state_index = 'A'
        #self.restarts = 0
        self.k = k
        self.kmeans = ts_cluster(k)

    #def make_state(self):
    #    ret = chr(ord(self.state_index)+1)
    #    self.state_index = ret
    #    return ret

    def pretrain(self, X):
        """ given a dataset X, pre - train the algorithm on X """
        self.kmeans.k_means_clust(X, 10, 200, True)

    def classify(self, msg, response):
        """ partial train algorithm and compute label given a response """
        #label = self.kmeans.predict(response)
        #self.signals.append((msg, response, label))
        pass

    def plot(self):
        self.kmeans.plot_centroids()
        print(self.kmeans.centroids)
        
