#!/usr/bin/python3.5
# pylint: disable=no-value-for-parameter
'''
created on: Dec. 19th 2018
author: John DiMatteo
description: 

smart algorithm to determine the validity of msgs in a specified protocol.
'''

import click
import random
#from cluster import cluster
#from I2C import...

@click.command()
@click.option('--protocol', '-p', default='i2c', help='protocol representing the format in which to fuzz. currently tested with i2c only.')
def fuzzer(protocol):
    # get msg format from json
    path_to_protocol = './protocols/' + str(protocol) + '.json'
    try:
        with open(path_to_protocol) as handle:
            #protocol_dict = json.loads(handle.read())

    except FileNotFoundError:
        click.echo("Incorrect protocol path entered. Please use a supported protocol in supported_protocols. See --help for more info.")
        exit()

    # for loop:

        # initialize msg class
        # msg = I2C_msg()
        # cluster = Clusterer()

        # msg.send()

        # wait()

        # response = msg.recieve()

        # cluster.fit(response)

        # depending on cluster info do  ...

    # print expected signal
    # cluster.expected_signal('group A')



    msg = {} # initialize msg
    for section in protocol_dict: # build first msg from random
        msg[section] = ''
        for i in range(protocol_dict[section]["size"]):
            msg[section] += str(random.randint(0,1))

    click.echo(msg)

    # ask msg <- in I2C.py


    # cluster the msg <- in cluster.py
    # print result <- in cluster.py
    pass

if __name__ == "__main__":
    fuzzer()