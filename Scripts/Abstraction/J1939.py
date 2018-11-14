#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 22 20:18:41 2018

@author: aaflores
"""

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

from can.interfaces.interface import Bus

from can.protocols import j1939


class J1939_Socket:
    
    def __init__(self,interface):
        self.bus = j1939.Bus(channel=interface, bustype='socketcan')

            
    def Send_Message(self, frame_id, frame_data):     
        arbitration_id = j1939.ArbitrationID(pgn=frame_id)
        message = j1939.PDU(arbitration_id=arbitration_id, data=bytearray.fromhex(frame_data))        
        self.bus.send(message)
                    
    def close(self):
        self.bus.shutdown()
        
        
"""
CHANGE LOG
_______________________________________
USER_ID   DATE      CHANGE_DESCRIPTION
_______________________________________

aaflores  05-22-18  -Initial file


"""
