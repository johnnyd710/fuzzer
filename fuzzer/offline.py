import os
import numpy as np
import click

LENGTH = 220
OFFSET = 0

class Offline():
    def __init__(self):
        click.echo("Offline mode activated.")
        self.signals = []

    def load(self, msg, directory = 'data/'):
        """ gets signals from specified directory """

        n=0

        path = directory + msg

        for filename in os.listdir(path):
            filename = path + '/' + filename
            self.signals.append((msg, np.genfromtxt(filename, delimiter=',')))
            n+=1
        click.echo("%d signals loaded from message %s" % (n, msg))        

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
