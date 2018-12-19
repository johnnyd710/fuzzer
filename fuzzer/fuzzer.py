#!/usr/bin/python3.5
'''
created on: Dec. 19th 2018
author: John DiMatteo
description: 

smart algorithm to determine the validity of msgs in a specified protocol.
'''

import click
#from cluster import cluster
#from I2C import...

@click.command()
@click.option('--protocol', '-p', default='i2c', help='protocol to fuzz. currently supports: i2c.')
def fuzzer(protocol):
    # get msg format from json
    if protocol == 'i2c':
        pass
    # create msg  
    # ask msg <- in I2C.py
    # cluster the msg <- in cluster.py
    # print result <- in cluster.py
    click.echo("Hello world!")
    pass

if __name__ == "__main__":
    # pylint: disable=no-value-for-parameter
    fuzzer()