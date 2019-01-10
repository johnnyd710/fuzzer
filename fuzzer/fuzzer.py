'''
Data class holds the time series responses as numpy arrays in a dictionary.
structure:
data: dict of dicts, each dict indexed by the 'msg'. 
data['msg']: dict of a bool (membership: VALID/INVALID) 
and a list of numpy arrays (data: [1.4 1.5 1.6 etc])
'''

import numpy as np
import matplotlib.pyplot as plt
import click
import os
import sys
sys.path.insert(0, './clusterers')

class Fuzzer:
    def __init__(self, length):
        '''
        initialize with 
        '''
        self.data = np.zeros(1)
        self.msg_dict = {}
        self.length = length

    def add(self, signal, label):
        """ for use after sending a message. label is the msg name."""

        if np.sum(self.data) == 0:
            self.data = signal.reshape(1,self.length)

        else:
            self.data = np.concatenate((self.data, signal.reshape(1,self.length)))

        idx = self.data.shape[0]-1 # index where you just placed signal

        if label in self.msg_dict:
            click.echo("Signal already loaded for this message "+ label +". Please retry.")

        else: self.msg_dict[label] = {'membership': 0, 'data': idx}

    def clean(self):
        """ get rid of noisy signals, output msgs removed """
        pass

    def check_for_noise(self):
        """ stopping condition for first pass. are any signals noise? """
        return True

    def plot_all_signals(self, membership, save = False):
        idxs = []

        for msg, info in self.msg_dict.items():
            if info['membership'] == membership:
                idxs.append(info['data'])

        signals = self.data[idxs]

        avg = np.average(signals, axis=0)
        std = np.std(signals, axis=0)
        x = range(self.length)
    
        plt.style.use('ggplot') #Change/Remove This If you Want
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.plot(x, avg, alpha=0.5, color='red', label=str(membership), linewidth = 1.0)
        ax.fill_between(x, avg - std, avg + std, color='#888888', alpha=0.4)
        ax.fill_between(x, avg - 2*std, avg + 2* std, color='#888888', alpha=0.2)
        ax.legend(loc='best')
        ax.set_ylabel("Signal units?")
        ax.set_xlabel("Time")
        if save: plt.savefig('../tests/figs/' +str(membership) + '.png')
        plt.show()

    def plot_signal(self, msg, save = False):
        """ plot expected signal given a msg """
        signal = self.data[msg]['data']
        x = range(signal.shape[0])
    
        plt.style.use('ggplot') #Change/Remove This If you Want
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.plot(x, signal, alpha=0.5, color='red', label=str(msg), linewidth = 1.0)
        ax.set_ylabel("Signal units?")
        ax.set_xlabel("Time")
        if save: plt.savefig('../tests/figs/' +str(msg)+ '.png')
        plt.show()
