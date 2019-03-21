#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
author: john dimatteo

desc:
recieves a sequence of messages,
then sends them one by one to the device

"""

from redis import Redis
import time
from I2C import I2C_Bus as Device
# from test import Mapper_Test as Device

HOST= '192.168.6.1'
PORT=6379


def main():

    r = Redis(host=HOST, port=PORT, db=0)
    p = r.pubsub()
    p.subscribe('Comms')

    Mapper = Device()

    while True:
        message = p.get_message()
        if message and message['data'] != 1:
            # do something
            time.sleep(0.3)
            Mapper.Map(message['data'].decode())
            print('Message %s Sent' % message['data'].decode())

        time.sleep(0.01)

    p.close()

    exit()


if __name__ == "__main__":
    main()
