#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 11:52:36 2018

@author: aaflores

Start the inteface in a console using the following command:
    
    sudo ip link set <interface> up type can bitrate <bitrate>
    
    parameter examples:
    <interface> = can0
    <bitrate> = 1000000
    
    
"""

import socket, sys, struct, can


class CAN_Socket:
    __can_init = 0
    __CAN_Socket =  socket.socket(socket.PF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
    __interface_name = "none"
    
    def __init__(self,interface):
        #Open CAN socket
        try:
            self.__CAN_Socket.bind((interface,))
            self.__can_init = 1
            print("Interface '%s' is now binded" % interface)
            self.__interface_name = interface
        except OSError:
            sys.stderr.write("Could not bind to interface '%s'\n" % interface)
            self.__can_init = 0
            exit
            
    def Send_Message(self, frame_id, frame_data):
        if self.__can_init:
            fmt = "<IB3x8s"
            can_pkt = struct.pack(fmt, frame_id, len(frame_data.encode()), frame_data.encode())
            self.__CAN_Socket.send(can_pkt)
        else:
            print("CAN Socket not binded")
                    
    def __del__(self):
        #only close the ocket if it was initialized
        if self.__can_init:  
            self.__CAN_Socket.close()
            print("%s Socket closed\n" % self.__interface_name)
        
        
"""
CHANGE LOG
_______________________________________
USER_ID   DATE      CHANGE_DESCRIPTION
_______________________________________

aaflores  05-17-18  -Initial file

aaflores  05-22-18  -Changed socket to j1939

aaflores  05-22-18  -Changed socket back to CAN

"""
