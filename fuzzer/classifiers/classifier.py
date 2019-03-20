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
import matplotlib.animation as animation
import matplotlib.pyplot as plt

PATH_TO_CENTROIDS = "../out/centroids-old"
LABEL_CHANNEL = "label"
TRACE_CHANNEL = "trace"
REDIS_HOST = "192.168.6.1"
NO_CLUSTERS = 5


def animate(i, p, classifier):
    message = p.get_message()
    if message:
        trace = np.fromstring(message['data'])
        label = classifier.classify(trace)
        # r.publish(LABEL_CHANNEL, label)
        ax.clear()
        ax.plot(trace)
        plt.ylabel("Power Consumption")
        plt.xlabel("Time Units")
        plt.title("Signal, cluster = " + str(label))


def main():

    r = Redis(host=REDIS_HOST, port=6379, db=0)
    p = r.pubsub()
    p.subscribe(TRACE_CHANNEL)

    _ = p.get_message()

    classifier = Kmeans(NO_CLUSTERS)
    # load in the offline model
    classifier.load_centroids(PATH_TO_CENTROIDS)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ani = animation.FuncAnimation(fig, animate, fargs=(p, classifier), interval=500)
    plt.show()

    p.close()
    exit()


if __name__ == "__main__":
    main()
