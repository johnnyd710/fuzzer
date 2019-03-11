#!/usr/bin/python3.5

import csv
import sys

def split(channelA, channelB, out, downsample_div=1):
    downsample_div = int(downsample_div)
    #test_file = open(channelA,"rb")
    #data = test_file.readline()

    counter = 1

    pulse_counter = 0
    signal_counter = 0
    file_open = 0
    signal_detected = 0
    indices = []
    end_indices = []
    start_writing = 0
    up=0
    c=0

    # goes through file, detects starting positions
    # detect start and end instead for channel A
    print("Detecting signals starting points...")
    for signal in channelA:

        if signal <= -200:
            up = 1

        if signal > -200 and up and signal_detected == 0:
            up=0
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
        c+=1

    signal_counter = 0
    internal_counter = 0
    num_signals = len(indices)
    print("No. of signals:", num_signals)

    i=0
    n=0
    c=0
    # cut channel B
    print("Splitting signals...", indices, "to", end_indices)
    for signal in channelB:
        c+=1
        if c < indices[i]:
              continue
        
        if file_open == 0:
              file_name = out + ".csv"
              current_csv = open(file_name, "w")
              file_open = 1

        if (n % downsample_div == 0):
            current_csv.write("%.13f \n" % (signal))

        if c >= (end_indices[i]):
              internal_counter = 0
              current_csv.close()
              file_open = 0
              signal_counter += 1
              i+=1

        if signal_counter >= num_signals:
              break
        n+=1

