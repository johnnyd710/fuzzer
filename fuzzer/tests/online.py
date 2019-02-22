'''
test the online ability of the system without the learner.
send a random msg, 
translate with mapper,
capture the trace, stream it through redis
display it and then repeat.
'''

import subprocess
import time
from redis import Redis
import matplotlib.pyplot as plt

PATH_TO_MAPPER = '../mappers/mapper.py'
PATH_TO_CLASSIFIER = '../classifiers/classifier.py'
LABEL_CHANNEL = 'label'
COMMS_CHANNEL = 'Comms'
WAIT = True

r = Redis(host='localhost', port=6379, db=0, decode_responses=True)
p = r.pubsub()
p.subscribe(COMMS_CHANNEL)
p.subscribe(LABEL_CHANNEL)

# start mapper
mapper = subprocess.Popen(PATH_TO_MAPPER)

# wait for subprocess to subscribe
while not p.get_message():
    pass

# start classifier
classifier = subprocess.Popen(PATH_TO_CLASSIFIER)

# wait for subprocess to subscribe
while not p.get_message():
    pass

p.unsubscribe(COMMS_CHANNEL)

while WAIT:
    try:
        message = p.get_message()
        if message:
            print(message['data'])
            plt.plot(message['data'])
            plt.show()

        time.sleep(0.1)

    except KeyboardInterrupt:
        r.publish(COMMS_CHANNEL, 'kill')
        mapper.kill()
        classifier.kill()
        p.close()
