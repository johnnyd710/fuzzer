#!/usr/bin/python3.5

import csv
import sys
import numpy as np


def np_split(channelA, channelB, out, downsample_div=1):
    downsample_div = int(downsample_div)

    counter = 1

    pulse_counter = 0
    signal_counter = 0
    file_open = 0
    signal_detected = 0
    indices = []
    end_indices = []
    start_writing = 0
    up = 0
    c = 0

    # goes through file, detects starting positions
    # detect start and end instead for channel A
    print("Detecting signals starting points...")
    for signal in channelA:

        if signal <= -200:
            up = 1

        if signal > -200 and up and signal_detected == 0:
            up = 0
            pulse_counter += 1
            if pulse_counter == 1:
                    signal_detected = 1
                    indices.append(c)
            if pulse_counter == 3:
                    pulse_counter = 0

        if up and signal_detected == 1:
            signal_detected = 0
            signal_counter += 1
            end_indices.append(c)

        if signal_counter >= 1000:
            break
        c += 1

    signal_counter = 0
    internal_counter = 0
    num_signals = len(indices)
    print("No. of signals:", num_signals)

    for idx, start in enumerate(indices):
        file_name = out + '-' + str(idx) + ".npy"
        arr = channelB[start:end_indices[idx]]
        # keep every (downsample_div)th value
        np.save(file_name, arr[::downsample_div])
