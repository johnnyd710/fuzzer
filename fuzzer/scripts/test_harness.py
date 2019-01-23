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

def main(eps, tol):
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
            
    for i in range(1000):
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
        #print(tmp)
        states_.append(max(tmp, key=tmp.get))
    
    #print(states_)

    from sklearn.metrics import confusion_matrix

    states_msgs = [states_[0], states_[0], states_[1], states_[2], states_[0], states_[0], states_[1], states_[2]]
    true = [states_msgs[msgs.index(m[0])] for m in Detector.signals] # for msg in detector signals put the equivalent state 0,1 or 2 as a list in true
    pred = [m[2] for m in Detector.signals]

    no_of_noise_samples = 0
    restarts = 0
    # remove noise from confusion matrix
    for idx, obs in enumerate(pred):
        if obs == None:
            no_of_noise_samples+=1
            true[idx] = None
        elif obs not in true:
            restarts += 1
            true[idx] = None
    
    # now remove from true:
    true = [e for e in true if e != None]

    # now remove from pred
    pred = [e for e in pred if e in true]

    #print("Noise samples= %d"% no_of_noise_samples)
    #print("Restarts = %d"% restarts)

    assert len(true) == len(pred)

    mat = confusion_matrix(true, pred)
    #print(mat)
    mat = np.asarray(mat)

    TP = np.diag(mat)
    FP = (np.sum(mat, axis=1)) - TP
    FN = (np.sum(mat, axis=0)) - TP
    Precision = TP / (TP+FP)
    Recall = TP / (TP+FN)
    F1 = 2 * (Precision*Recall) / (Recall + Precision)
    #print(np.average(F1))

    return(np.average(F1)*100, no_of_noise_samples, restarts)


if __name__ == "__main__":
    f1 = []
    noise = []
    restart = []

    tol = 200 
    for eps in range(0, 200, 10):
        f, n, r = main(eps, tol)
        f1.append(f)
        noise.append(n)
        restart.append(r)

    import matplotlib.pyplot as plt
    plt.plot(f1, label = "F1 Score")
    plt.plot(noise, label = "No. of Noise Samples")
    plt.plot(restart, label = "No. of Restarts")
    plt.legend()
    plt.title("Classifier Metrics with Epsilon Varied and Tolerance at "+ str(tol))
    plt.xlabel("Value of Epsilon (DTW Distance)")
    plt.ylabel("Percentage (%)")
    plt.show()


    eps = 100 
    for tol in range(100, 700, 30):
        f, n, r = main(eps, tol)
        f1.append(f)
        noise.append(n)
        restart.append(r)

        plt.plot(f1, label = "F1 Score")

    plt.plot(noise, label = "No. of Noise Samples")
    plt.plot(restart, label = "No. of Restarts")
    plt.legend()
    plt.title("Classifier Metrics with Tolerance Varied and Epsilon at "+ str(eps))
    plt.xlabel("Value of Tolerance (DTW Distance)")
    plt.ylabel("Percentage")
    plt.show()




    exit()

