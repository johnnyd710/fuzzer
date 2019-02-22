
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

PATH_TO_CENTROIDS = "../out/centroids"
PATH_TO_CAPTURE_SCRIPT = "../scripts/capture.sh"
PATH_TO_TRACE = "./trace"
LABEL_CHANNEL = "label"
COMMS_CHANNEL = "Comms"


def main():

    r = Redis(host='localhost', port=6379, db=0)
    p = r.pubsub()
    p.subscribe(COMMS_CHANNEL)

    classifier = Kmeans()
    # load in the offline model
    classifier.load_centroids(PATH_TO_CENTROIDS)

    while True:
        message = p.get_message()
        if message:
            # execute capture script
            subprocess.call([PATH_TO_CAPTURE_SCRIPT])
            file = open(PATH_TO_TRACE, 'rb')
            trace = np.fromfile(file, dtype=float)
            label = classifier.classify(trace)
            r.publish(LABEL_CHANNEL, label)
        time.sleep(0.001)

    p.close()
    exit()


if __name__ == "__main__":
    main()
