#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: john dimatteo

desc:
captures the trace from the digitizer and classifies it,
sending the classification to the learner through redis

"""

from redis import Redis
import time
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from downsample import downsample
from numpy_split import split

PATH_TO_CENTROIDS = "../out/centroids-old"
PATH_TO_CAPTURE_SCRIPT = "../../scripts/acquire_to_disk"
PATH_TO_TRACE = "/Digitizer/captured-data/"
LABEL_CHANNEL = "label"
COMMS_CHANNEL = "Comms"
TRACE_CHANNEL = "trace"
REDIS_HOST = "127.0.0.1"
POWERTRACE_LOG = "I2C_TEST"
CAPTURE_LENGTH = "3"
SAMPLE_RATE = "10"
INPUT_RANGE = "400mV"
DOWNSAMPLE_DIV = 50
DOWNSAMPLE_THROW = 50
PATH_TO_BIN2TXT = "../../scripts/bin2txt"
NO_CHANNELS = "2"
SPLIT_TRACE_PATH = "../out/traces/trace-"
BUFFER_SIZE = 2048000

def main():

    r = Redis(host=REDIS_HOST, port=6379, db=0)
    p = r.pubsub()
    p.subscribe(COMMS_CHANNEL)
    _ = p.get_message()

    while True:
        message = p.get_message()
        if message and message['data'] != 1:
            print(message['data'])
            # execute capture script
            now = datetime.now()
            start_capture = time.time()
            p1 = subprocess.Popen([PATH_TO_CAPTURE_SCRIPT, SAMPLE_RATE, 
                                   INPUT_RANGE,
                                   CAPTURE_LENGTH, 
                                   POWERTRACE_LOG, NO_CHANNELS])
            p1.wait()
            end_capture = time.time()
            time_format = now.strftime("%Y-%m-%d-%H%M")
            FULL_PATH_TO_TRACE = PATH_TO_TRACE + \
                                   time_format + \
                                          "--" + \
                                   SAMPLE_RATE + \
                                   "MSPS--"    + \
                                   INPUT_RANGE + \
                                          "--" + \
                                POWERTRACE_LOG
            start_bin = time.time()
            data = np.fromfile(FULL_PATH_TO_TRACE, dtype='uint16')
            data = (data - 32768.0)*400 / 32768
            arrays = np.split(data, data.shape[0] // BUFFER_SIZE)
            channelA = np.concatenate(arrays[0::2])
            channelB = np.concatenate(arrays[1::2])
            end_bin = time.time()
            #trace = np.genfromtxt(FULL_PATH_TO_TRACE + "--channel-A.txt", dtype=float, usecols = (1))
            #gpio = np.genfromtxt(FULL_PATH_TO_TRACE + "--channel-B.txt", dtype=float, usecols = (1))
            # SPLIT
            time_format = now.strftime("%Y-%m-%d-%H%M%S")
            start_split = time.time()
            no_signals = split(channelA, 
                  channelB,
                  SPLIT_TRACE_PATH + time_format,
                  DOWNSAMPLE_THROW)
            end_split = time.time()
            if no_signals == 0:
                print("No signal detected ... skipping message.\n")
                plt.plot(channelB)
                plt.show()
                continue
            start_load = time.time()
            traces = []
            for signal in range(1, no_signals+1):
                traces.append(np.load(SPLIT_TRACE_PATH + time_format + '-' + str(signal) + '.npy'))
            end_load = time.time()
            # DOWNSAMPLE
            start_downsample = time.time()
            if False:
                for trace in traces:
                    trace = downsample(trace, DOWNSAMPLE_DIV)
            end_downsample = time.time()
            #gpio = downsample(gpio, DOWNSAMPLE_DIV)
            print("capture time: ", end_capture - start_capture)
            print("BIN2TXT time : ", end_bin - start_bin)
            print("SPLIT time : ", end_split - start_split)
            print("load trace time : ", end_load - start_load)
            print("downsample (avg) time : ", end_downsample - start_downsample)
            print("TOTAL :", end_downsample - start_bin)
            # PLOT
            #plt.plot(gpio)
            for trace in traces:
                r.publish(TRACE_CHANNEL, trace.tostring())
                time.sleep(0.3)
        time.sleep(0.001)

    p.close()
    exit()


if __name__ == "__main__":
    main()
