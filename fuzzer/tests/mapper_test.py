'''
use a random learner (i.e. send random msgs)
and test the mappers ability to translate and send the input
'''

import subprocess
from redis import Redis

PATH_TO_MAPPER = '../mappers/mapper.py'
WAIT = True
# now act as a random learner
r = Redis(host='localhost', port=6379, db=0, decode_responses=True)
p = r.pubsub()
p.subscribe('Comms')

# start mapper 
process = subprocess.Popen(PATH_TO_MAPPER)

# wait for subprocess to subscribe
while not p.get_message():
    pass

msgs = ['start', 'this', 'test', 'is', 'successful']

for msg in msgs:
    # send first msg and wait for response
    r.publish('Comms', msg)
    while WAIT:
        message = p.get_message()
        if message:
            print(message['data'])
            break

r.publish('Comms', 'kill')

process.kill()

p.close()