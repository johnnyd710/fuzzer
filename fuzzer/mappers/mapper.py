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


def main():

    r = Redis(host='localhost', port=6379, db=0)
    p = r.pubsub()
    p.subscribe('Comms')

    Mapper = Device()

    while True:
        message = p.get_message()
        if message:
            # do something
            Mapper.Map(message['data'])

        time.sleep(0.01)

    p.close()

    exit()


if __name__ == "__main__":
    main()