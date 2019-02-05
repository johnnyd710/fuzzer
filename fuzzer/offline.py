import os
import numpy as np
import click



class Offline():
    def __init__(self):
        click.echo("Offline mode activated.")
        self.signals = []

    def first_load(self, directory, MIN_LENGTH):
        offset=1000 # min length to be accepted (assume below this is noise)
        list_of_signals = []
        n = 0

        for filename in os.listdir(directory):
            filename = directory + '/' + filename
            signal = np.genfromtxt(filename, delimiter=',')
            if len(signal) > MIN_LENGTH:
                list_of_signals.append(signal)
                n+=1            

        #MIN_LENGTH =MIN_LENGTH  // 100 * 100 # make it divisable by 100 for downsampling later

        # truncate each signal to same size
        for i, arr in enumerate(list_of_signals):
            arr = arr[int(offset):int(MIN_LENGTH)]
            list_of_signals[i] = arr #.reshape(l,1)

        print("Signals loaded. Length of a signal is %d, No. of signals is: %d" % (MIN_LENGTH, n))
        self.signals = list_of_signals

    def load_msg(self, msg, directory = '../data/'):
        """ gets signals from specified directory """

        signals=[]
        n=0
        path = directory + msg

        for filename in os.listdir(path):
            filename = path + '/' + filename
            signals.append(np.genfromtxt(filename, delimiter=','))
            n+=1
        click.echo("%d signals loaded from message %s" % (n, msg))

        return signals        

    def load(self, path):
        """ gets signals from specified directory """

        n=0

        for filename in os.listdir(path):
            filename = path + '/' + filename
            self.signals.append(np.genfromtxt(filename, delimiter=','))
            n+=1
        click.echo("%d signals loaded from %s" % (n, path))   

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
        downsampled_signals = []
        
        for i, signal in enumerate(signals):
            downsampled_signals.append(self.downsample(signal, div))
            
        return downsampled_signals

    def write_out(self, out_dir, create=False):
        # Example
        if create:
            self.createFolder(out_dir)

        for i, sig in enumerate(self.downsample_signals(np.array(self.signals))):
            np.savetxt(out_dir + str(i), sig, delimiter=',')

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
