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
from kmeans import Kmeans
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from downsample import downsample
from split import split

PATH_TO_CENTROIDS = "../out/centroids"
PATH_TO_CAPTURE_SCRIPT = "../../scripts/acquire_to_disk"
PATH_TO_TRACE = "/Digitizer/captured-data/"
LABEL_CHANNEL = "label"
COMMS_CHANNEL = "Comms"
REDIS_HOST = "192.168.6.1"
POWERTRACE_LOG = "I2C_TEST"
CAPTURE_LENGTH = "1"
SAMPLE_RATE = "10"
INPUT_RANGE = "400mV"
DOWNSAMPLE_DIV = "100"
PATH_TO_BIN2TXT = "../../scripts/bin2txt"
NO_CHANNELS="2"
SPLIT_TRACE_PATH = "../out/traces/trace-"


def main():

    r = Redis(host=REDIS_HOST, port=6379, db=0)
    p = r.pubsub()
    p.subscribe(COMMS_CHANNEL)

    _ = p.get_message()

    #classifier = Kmeans()
    # load in the offline model
    #classifier.load_centroids(PATH_TO_CENTROIDS)

    while True:
        message = p.get_message()
        if message:
            # execute capture script
            subprocess.call([PATH_TO_CAPTURE_SCRIPT, SAMPLE_RATE, 
                             INPUT_RANGE,
                             CAPTURE_LENGTH, 
                             POWERTRACE_LOG, NO_CHANNELS])
            now = datetime.now()
            time_format = now.strftime("%Y-%m-%d-%H%M")
            FULL_PATH_TO_TRACE = PATH_TO_TRACE + \
                                   time_format + \
                                          "--" + \
                                   SAMPLE_RATE + \
                                   "MSPS--"    + \
                                   INPUT_RANGE + \
                                          "--" + \
                                POWERTRACE_LOG

            subprocess.call([PATH_TO_BIN2TXT, NO_CHANNELS, FULL_PATH_TO_TRACE, 
                             SAMPLE_RATE, INPUT_RANGE])

            #trace = np.genfromtxt(FULL_PATH_TO_TRACE + "--channel-A.txt", dtype=float, usecols = (1))
            #gpio = np.genfromtxt(FULL_PATH_TO_TRACE + "--channel-B.txt", dtype=float, usecols = (1))
            # SPLIT
            split(FULL_PATH_TO_TRACE + "--channel-A.txt", 
                  FULL_PATH_TO_TRACE + "--channel-B.txt",
                  SPLIT_TRACE_PATH + time_format)
            
            trace = np.genfromtxt(SPLIT_TRACE_PATH + time_format + '.csv', dtype=float)
            # DOWNSAMPLE
            trace = downsample(trace, DOWNSAMPLE_DIV)
            #gpio = downsample(gpio, DOWNSAMPLE_DIV)
            print("Trace Length: ")
            print(trace.shape)
            # PLOT
            plt.plot(trace)
            #plt.plot(gpio)
            plt.show()
            #label = classifier.classify(trace)
            #r.publish(LABEL_CHANNEL, label)
        time.sleep(0.001)

    p.close()
    exit()


if __name__ == "__main__":
    main()
