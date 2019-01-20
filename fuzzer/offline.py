import os
import numpy as np
import click

LENGTH = 220
OFFSET = 0

class Offline():
    def __init__(self):
        click.echo("Offline mode activated.")

    def load(self, directory):
        '''
        gets signals from specified directory 
        and returns a (n, l, 1) numpy array
        where n is number of distinct signals and
        l is length of each signal.
        '''

        list_of_signals = []

        n = 0

        for filename in os.listdir(directory):
            filename = directory + '/' + filename
            list_of_signals.append(np.genfromtxt(filename, delimiter=','))
            n+=1
        
        no_signals = len(list_of_signals) # comment out if doing subsampling for testing
        
        signals = np.zeros([no_signals-1, LENGTH])   # replace 5 with n ! 
        
        for i, arr in enumerate(list_of_signals[1:(no_signals-1)]):
            arr = arr[OFFSET:LENGTH+OFFSET]
            signals[i][0:arr.shape[0]] = arr

        self.signals = signals
        self.index = 0
        self.directory = directory

    def get_signal(self, msg):
        directory = './data/' + msg
        files = os.listdir(directory)
        filename = np.random.choice(files, size = 1)[0]
        path = directory + '/' + filename
        return np.genfromtxt(path, delimiter=',')    

    def downsample(self, s, R):
        s = s.reshape(-1, R)
        return s.reshape(-1, R).mean(axis=1)

    def downsample_signals(self, signals, div = 100):
        downsampled_signals = np.zeros([signals.shape[0], LENGTH//div])
        
        for i, signal in enumerate(signals):
            downsampled_signals[i] = self.downsample(signal, div)
            
        return downsampled_signals

    def write_out(self, out_dir, name, create=False):
        # Example
        if create:
            self.createFolder(out_dir)

        for i, sig in enumerate(self.downsample_signals(self.signals)):
            np.savetxt(out_dir + '/' + name + str(i), sig, delimiter=',')

    def createFolder(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print('Error: Creating directory. ' +  directory)

    def plot(self, sig):
        import matplotlib.pyplot as plt
        plt.plot(sig)
        plt.show()