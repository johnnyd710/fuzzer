"""
this goes ON the device
"""

from abc import ABC, abstractmethod
import numpy as np
import csv 

class MessageSender(ABC):
    def __init__(self, name):
        '''
        initialize with 
        '''
        self.vocab = []
        super().__init__()

    def save(self, filename):
        with open(filename + '.csv', 'w') as fh:
            writer = csv.writer(fh, delimiter=',')
            writer.writerow(['id','val'])
            writer.writerows(enumerate(self.clus))

    def load(self, filename):
        self.clus = np.loadtxt(filename + '.csv', skiprows=1, usecols=1, delimiter=',')

    @abstractmethod
    def plot_clusters(self):
        pass

    @abstractmethod
    def cluster(self):
        pass
    