#!/usr/bin/python3.5

'''
created on: Jan. 21st 2019
author: John DiMatteo
description: 
'''

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import sys
sys.path.insert(0,'../')

import click
from state_detector import State_Detector
from offline import Offline
import numpy as np
import os
import matplotlib.pyplot as plt

def main(eps, tol, sample_size=500):
    # initialize
    Detector = State_Detector(eps=eps, tol=tol)

    # determine which message to send
    # send the message

    # get response (offline for now)
    msgs = ['reg0-bar', 'reg0-alt', 'reg0-bar-active', 'reg0-alt-active',
            'reg1-bar', 'reg1-alt', 'reg1-bar-active', 'reg1-alt-active']

    signals = {msg:[] for msg in msgs}

    n=0

    for msg in msgs:
        directory = '../data/' + msg
        files = os.listdir(directory)
        for filename in files:
            n+=1
            path = directory + '/' + filename
            signals[msg].append(np.genfromtxt(path, delimiter=','))
            # process response 
            
    for i in range(sample_size):
        msg = np.random.choice(msgs)
        if len(signals[msg]) != 0:
            response = signals[msg].pop()       
            Detector.classify(msg, response)

    from collections import Counter

    #print("Detector Index at:", Detector.state_index)

    # organize into states
    standby = ['reg0-bar', 'reg1-bar', 'reg0-alt', 'reg0-bar']
    barometer = ['reg0-bar-active', 'reg1-bar-active']
    altimeter = ['reg0-alt-active', 'reg1-alt-active']
    states = [standby, barometer, altimeter]
    states_=[]

    for i in range(3):
        tmp = Counter(obs[2] for obs in Detector.signals if obs[0] in states[i])
        del tmp[None]
        if sum(tmp.values()):
            max_val = max(tmp, key=tmp.get)
            if max_val not in states_:
                states_.append(max_val)
            else:
                states_.append('Nothing')
        else:
            states_.append('Nothing')
    
    restarts = Detector.restarts

    from sklearn.metrics import confusion_matrix

    # for each msg, write the state label that best represents it
    states_msgs = [states_[0], states_[0], states_[1], states_[2], states_[0], states_[0], states_[1], states_[2]]
    
    # for msg in detector signals put the equivalent state 0,1 or 2 as a list in true
    true = [states_msgs[msgs.index(m[0])] for m in Detector.signals] 
    pred = [m[2] for m in Detector.signals]

    no_of_noise_samples = 0
    # remove noise from confusion matrix
    for idx, obs in enumerate(pred):
        if obs == None:
            no_of_noise_samples+=1
            true[idx] = None
    
    # now remove from true:
    true = [e for e in true if e != None]

    # now remove from pred
    pred = [e for e in pred if e != None]
    mat = confusion_matrix(true, pred, labels=list(set(pred)))
    print(mat)
    mat = np.asarray(mat)

    TP = np.diag(mat)
    FP = np.sum(mat, axis=1) - TP
    FN = np.sum(mat, axis=0) - TP
    TP, FP, FN = np.sum(TP), np.sum(FP), np.sum(FN)
    Precision = TP / (TP+FP)
    Recall = TP / (TP+FN)
    F1 = 2 * (Precision*Recall) / (Recall + Precision) # MICRO
    #print(np.average(F1))

    return(F1*100, no_of_noise_samples, restarts)


if __name__ == "__main__":
    tol = 400
    x_range = np.arange(0,1000,25)

    f1 = []
    noise = []
    restart = []
    for eps in x_range:
        f, n, r = main(eps, tol)
        f1.append(f)
        noise.append(n)
        restart.append(r)

    plt.style.use('ggplot')

    plt.plot(x_range, f1, label = "F1 Score")
    plt.xlabel("Distance")
    plt.ylabel("Percentage (%)")
    plt.savefig('../../Documents/figs/eps.png')
    plt.clf()
    
    plt.plot(x_range, restart, label = "No. of Restarts")
    plt.plot(x_range, noise, label = "No. of Noise Samples")
    plt.xlabel("Distance")
    plt.ylabel("Count")
    plt.legend()
    plt.savefig('../../Documents/figs/eps-other.png')
    plt.clf()

    f1 = []
    noise = []
    restart = []

    eps = 200 
    x_range = np.arange(0,1000,25)
    for tol in x_range:
        f, n, r = main(eps, tol)
        f1.append(f)
        noise.append(n)
        restart.append(r)

    plt.plot(x_range, f1, label = "F1 Score")
    plt.xlabel("Distance")
    plt.ylabel("Percentage (%)")
    plt.savefig('../../Documents/figs/tol.png')
    plt.clf()

    plt.plot(x_range, restart, label = "No. of Restarts")
    plt.plot(x_range, noise, label = "No. of Noise Samples")
    plt.xlabel("Distance")
    plt.ylabel("Count")
    plt.legend()
    plt.savefig('../../Documents/figs/tol-other.png')
    plt.clf()

#TODO: add y axis for counts
# noise sample line is constant?
