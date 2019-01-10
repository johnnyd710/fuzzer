import sys
import numpy as np
import os
sys.path.insert(0, '../fuzzer/clusterers')
#from pearson import Pearson
#from gmm import GMM
#from dtw import DTW
import random
import matplotlib.pyplot as plt

min_length = 26707

'''
todo : change get_signals as a function inside cluster? so that min length can be set in there?
'''

def plot_signals(signals, name):
    avg = np.average(signals, axis=0)
    std = np.std(signals, axis=0)
    x = range(signals.shape[1])

    plt.style.use('ggplot') #Change/Remove This If you Want
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.plot(x, avg, alpha=0.5, color='red', label=name, linewidth = 1.0)
    ax.fill_between(x, avg - std, avg + std, color='#888888', alpha=0.4)
    ax.fill_between(x, avg - 2*std, avg + 2* std, color='#888888', alpha=0.2)
    ax.legend(loc='best')
    ax.set_ylabel("Signal units?")
    ax.set_xlabel("Time")
    plt.savefig('./figs/' + name + '.png')
    plt.show()

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
    signals1 = get_signals('../Scripts/Applications/Data_processing/signals', 100)
    plot_signals(signals1, 'wrong-address')
    signals2 = get_signals('../Scripts/Applications/Data_processing/signals-2', 100)
    plot_signals(signals2, 'active-registers')
    
    exit()


    all_signals = np.concatenate((signals1, signals2))
    #clusterer = Pearson('wrong-address-vs-valid', signals2)
    #clusterer = GMM('wrong-address-vs-valid-GMM', signals2)
    clusterer = DTW('wrong-address-vs-valid', signals1)
    clusterer.add_data(signals2)
    clusterer.cluster()
    #clusterer.save('valid-invalid')
    clusterer.plot_clusters()

