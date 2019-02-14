"""
this goes ON the device
"""

from abc import ABC, abstractmethod
import numpy as np
import csv 

class Mapper(ABC):
    def __init__(self, name):
        '''
        initialize with 
        '''
        super().__init__()

    def save(self, filename):
        with open(filename + '.csv', 'w') as fh:
            writer = csv.writer(fh, delimiter=',')
            writer.writerow(['id','val'])
            writer.writerows(enumerate(self.clus))

    def load(self, filename):
        self.clus = np.loadtxt(filename + '.csv', skiprows=1, usecols=1, delimiter=',')

    @abstractmethod
    def Send_Message_To_System(self):
        pass

    @abstractmethod
    def Map(self):
        pass
    