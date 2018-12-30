import sys
import numpy as np
import os
sys.path.insert(0, '../fuzzer/clusterers')
from pearson import Pearson
from gmm import GMM
from dtw import DTW
import random

min_length = 26707

'''
todo : change get_signals as a function inside cluster? so that min length can be set in there?
'''

def get_signals(dir, max_no_signals = 10):
    '''
    gets signals from specified directory 
    and returns a (n, l, 1) numpy array
    where n is number of distinct signals and
    l is length of each signal.
    '''
    directory = dir

    list_of_signals = []

    n = 0
    for filename in os.listdir(directory):
        filename = directory + '/' + filename
        list_of_signals.append(np.genfromtxt(filename, delimiter=','))
        n+=1
    
    min_l = 1e10
    for s in list_of_signals:
        l = len(s)
        if l < min_l: min_l = l

    signals = np.zeros([max_no_signals, min_length])   # replace 5 with n ! 

    sel = random.sample(list_of_signals, max_no_signals)
    for i, arr in enumerate(sel):
        arr = arr[0:min_length]
        signals[i] = arr #.reshape(l,1)

    print("Signals loaded. Length of a signal is",len(signals[0]))
    return signals


if __name__ == '__main__':
    print('testing clustering...')
    signals1 = get_signals('../Scripts/Applications/Data_processing/signals')
    #clusterer = Pearson('wrong-address-vs-valid', signals2)
    #clusterer = GMM('wrong-address-vs-valid-GMM', signals2)
    clusterer = DTW('wrong-address-vs-valid', signals1)
    signals2 = get_signals('../Scripts/Applications/Data_processing/signals-2')
    clusterer.add_data(signals2)
    clusterer.cluster()
    #clusterer.save('valid-invalid')
    clusterer.plot_clusters()

