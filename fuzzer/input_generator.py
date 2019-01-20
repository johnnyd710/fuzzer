#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
created on: Jan. 19th 2019
author: John DiMatteo
description: 

determines which input to send
should be smart enough to know which operations & message format gets the best system response, 
by developing rules and generalizing
(ie. for i2c MPL chip, addr 60 is necessary, control registers are necessary, and data packets flipping bits are the best)
     for URL, characters are necessary

possilibities:
-- form of active learning
-- genetic algorithms?

data:
-- dict of 'message': 'result'

example output:
--  ADR     REG         DATA        DESC
    0x60    -           -           valid adrs
    0x60    0x01..0x45  -           active regs
    0x60    0x26        0x01        mode switch
    0x60    0x26        0x80        mode switch

'''

class Input_Generator:
    
    def __init__(self, protocol):
        #TODO put this in a json file, one for each protocol
        if protocol == 'i2c':
            self.protocol = {'adr': {'min': 0, 'max': 255, 'type': int}, 'reg': {'min': 0, 'max': 255, 'type': int}, 'data':{'min': 0, 'max': 255, 'type': int}}

        self.knowledge = {}
        self.rules = {}

    def generalize(self):
        pass     

    def reset(self):
        pass   

    def increment(self):
        pass

    def decrement(self):
        pass

    def flip_bit(self, pos):
        pass
        