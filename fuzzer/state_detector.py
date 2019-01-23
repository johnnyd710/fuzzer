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

from sklearn.cluster import DBSCAN

def dtw(x, y):
    distance, path = fastdtw(x, y, dist=1)
    return distance

class State_Detector:
    
    def __init__(self, eps=100, tol = 600):
        """ signals is a list of tuples : [(msg,response, label)]"""
        self.signals = []
        self.state_index = 'A'
        self.eps = eps
        self.tol = tol

    def make_state(self):
        ret = chr(ord(self.state_index)+1)
        self.state_index = ret
        return ret

    def merge(self, l):
        for idx, obs in enumerate(self.signals):
            if obs[2] in l:
                obs[2] = l[0]
        return l[0]

    def classify(self, msg, response):
        """ compute similarity to each label, which is the mean similarity of all the labels members. append (msg, response, best matching label) to self.signals """
        new_label = None
        if len(self.signals) == 0:
            new_label = self.state_index

        else:
            distances = {key:0 for key in set(e[2] for e in self.signals if e[2] != None)}
            for label in distances:
                signals = [s[1] for s in self.signals if s[2] == label] # get all signals with the same label as a list
                distance = 0
                for n, signal in enumerate(signals):
                    distance += dtw(response, signal)
                distance /= (n+1)
                distances[label] = distance
            
            closest_labels = []
            for label, dist in distances.items(): 
                if dist < self.eps: 
                    closest_labels.append(label)

            if len(closest_labels)==0: 
                # make a new state if it isnt noise
                closest = min(distances, key=distances.get)
                if distances[closest] < self.tol:
                    new_label = self.make_state()
                    #click.echo('New State Detected! Distance to closest state = %d. New state = %s' % (distances[closest], self.state_index))

            elif len(closest_labels)==1:
                # assign to closest state
                new_label = closest_labels[0]

            elif len(closest_labels)>1:
                new_label = self.merge(closest_labels)
                #click.echo('Merging states: %s to %s' % (closest_labels, new_label))

        self.signals.append([msg, response, new_label])
  
