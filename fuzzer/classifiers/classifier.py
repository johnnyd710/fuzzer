#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: john dimatteo

desc:
captures the trace from the digitizer and classifies it,
sending the classification to the learner through redis

"""
import time
from redis import Redis
from kmeans import Kmeans
import numpy as np

PATH_TO_CENTROIDS = "../out/centroids-old"
LABEL_CHANNEL = "label"
TRACE_CHANNEL = "trace"
REDIS_HOST = "192.168.6.1"
NO_CLUSTERS = 5

def main():

    r = Redis(host=REDIS_HOST, port=6379, db=0)
    p = r.pubsub()
    p.subscribe(TRACE_CHANNEL)

    _ = p.get_message()

    classifier = Kmeans(NO_CLUSTERS)
    # load in the offline model
    classifier.load_centroids(PATH_TO_CENTROIDS)

    while True:
        message = p.get_message()
        if message:
            trace = np.fromstring(message['data'])
            label = classifier.classify(trace)
            print("LABEL is: ", label)
            #r.publish(LABEL_CHANNEL, label)
        time.sleep(0.001)

    p.close()
    exit()


if __name__ == "__main__":
    main()
