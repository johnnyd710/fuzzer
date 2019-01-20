#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
created on: Jan. 19th 2019
author: John DiMatteo
description: 

determine state change

data:
-- previous responses from the system

psuedocode:

'''
from fastdtw import fastdtw
import numpy as np
import click

def dtw(x, y):
    distance, path = fastdtw(x, y, dist=1)
    return distance

class Change_Detector:
    
    def __init__(self, eps=1):
        self.past_response = np.array([])
        self.eps = eps

    def similarity(self, response, metric = dtw):
        '''
        using a similarity metric calculate the similarity between the past response and the current one
        '''
        return metric(self.past_response, response)

    def update(self, response):
        ''' TODO: add multiple metrics for robustness (corr, euclid), noise threshold '''
        similarity = self.similarity(response)

        if self.past_response.size == 0:
            self.past_response = response

        elif similarity > self.eps:
            click.echo('State Change Detected! Distance = %d' % similarity)
            self.plot(response)
            self.past_response = response

    def plot(self, signal):
        import matplotlib.pyplot as plt
        plt.plot(self.past_response, label = 'last response')
        plt.plot(signal, label = 'new response')
        plt.legend()
        plt.show()        

        