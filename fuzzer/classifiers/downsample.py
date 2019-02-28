#!/usr/bin/python3.5

import numpy as np
import math

def downsample(signal, div=100):
    div = int(div)
    pad = math.ceil(float(signal.size)/div)*div - signal.size
    signal_padded = np.append(signal, np.zeros(pad)*np.NaN)
    return np.nanmean(signal_padded.reshape(-1, div), axis=1)
