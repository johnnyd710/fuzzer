#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=no-value-for-parameter
'''
created on: Jan. 19th 2019
author: John DiMatteo
description: 

sends an input to the system/device

psuedocode:

'''

import smbus

class I2C_Bus:
    
    def __init__(self,interface):
        self.bus = smbus.SMBus(int(interface))
        
    def Send_Message(self, device_address, data, register_offset=0):         
        list = [int(str(data),16)]         
        self.bus.write_i2c_block_data(int(str(device_address),16),int(str(register_offset),16), list)     

    def Recieve_Message(self, device_address, register_offset):         
        # read a block of 16 bytes from address device_address with offset register_offset         
        data = self.bus.read_i2c_block_data(int(str(device_address),16), int(str(register_offset),16), 16) # (int address, char cmd)         
        return data
                    
    def close(self):
        x=0 #dummy operation
        

"""
CHANGE LOG
_______________________________________
USER_ID   DATE      CHANGE_DESCRIPTION
_______________________________________

aaflores  Jul-09-18  -Changed name of file to capital letters
		     -Removed debugging code


"""