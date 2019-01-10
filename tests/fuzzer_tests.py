import sys
import numpy as np
import os
import random

sys.path.insert(0, '../fuzzer/')
sys.path.insert(0, '../fuzzer/protocols')

from fuzzer import Fuzzer
from i2c_msg import I2C_Msg

min_length = 26707

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

    sel = random.sample(os.listdir(directory), max_no_signals)

    for filename in sel:
        filename = directory + '/' + filename
        list_of_signals.append(np.genfromtxt(filename, delimiter=','))
        n+=1
    
    min_l = 1e10
    for s in list_of_signals:
        l = len(s)
        if l < min_l: min_l = l

    signals = np.zeros([max_no_signals, min_length])   # replace 5 with n ! 

    for i, arr in enumerate(list_of_signals):
        arr = arr[0:min_length]
        signals[i] = arr #.reshape(l,1)

    print("Signals loaded. Length of a signal is",len(signals[0]))
    return signals


if __name__ == '__main__':
    print('testing...')
    signals1 = get_signals('../Scripts/Applications/Data_processing/signals', 2)
    signals2 = get_signals('../Scripts/Applications/Data_processing/signals-2', 2)
    
    Fuzzer = Fuzzer()
    I2C_Msg = I2C_Msg()

    for signal in signals1:
        # address swipe 68 
        n=0
        Fuzzer.offline_add(signal, I2C_Msg.out(68, n))
        n+=1

    for signal in signals1:
        # address swipe 68 
        n=0
        Fuzzer.offline_add(signal, I2C_Msg.out(60, 1))
        n+=1

    Fuzzer.plot_signal(I2C_Msg.out(60, 1))
    