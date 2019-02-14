"""
-- this will be on the system (raspberry pi, arduino, etc.)
recieves a query in the form 'address/register/data'
and sends an I2C message with those parameters.
"""

from mapper import Mapper
import smbus

class I2C_Bus(Mapper):
    """  recieves messages from Input Generator and sends them to system in a way the system can understand  """
    
    def __init__(self, interface):
        """ vocab should be a list of strings formatted as follows: 
        [ADR1/REG1/DATA1, ADR1/REG1/DATA2 ... etc.] 
        representing the available input space"""
        super().__init__()
        self.bus = smbus.SMBus(int(interface))
        
    def Send_Message_To_System(self, device_address, data, register_offset=0):        
        list = [int(str(data),16)]         
        self.bus.write_i2c_block_data(int(str(device_address),16),int(str(register_offset),16), list)     

    def Recieve_Message_From_System(self, device_address, register_offset):         
        # read a block of 16 bytes from address device_address with offset register_offset         
        data = self.bus.read_i2c_block_data(int(str(device_address),16), int(str(register_offset),16), 16) # (int address, char cmd)         
        return data
                    
    def Close(self):
        pass

    def Map(self, msg):
        """ consume (msg) a string in the form ADR/REG/DATA and translate to I2C Message """
        address, register, data = msg.split("/")
        self.Send_Message_To_System(address, data, register)
