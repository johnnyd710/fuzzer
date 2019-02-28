"""
-- this will be on the system (raspberry pi, arduino, etc.)
recieves a query in the form 'address/register/data'
and sends an I2C message with those parameters.
"""
import time
import smbus
import Adafruit_BBIO.GPIO as GPIO


class I2C_Bus():
    """  recieves messages from Input Generator and sends them to system in a way the system can understand  """

    def __init__(self, interface='2'):
        """ vocab should be a list of strings formatted as follows:  
        [ADR1/REG1/DATA1, ADR1/REG1/DATA2 ... etc.] 
        representing the available input space"""
        super().__init__()
        self.bus = smbus.SMBus(int(interface))

    def Process_Message(self, msg):
        op, adr, reg, data = msg.split("/")
        GPIO.setup("P8_7", GPIO.OUT)
        if op == 'w':
            self.HIGH_LOW(0.02)
            self.Send_Message_To_System(adr, reg, data)
            self.HIGH_LOW(0.01)
            self.HIGH_LOW(0.01)
        else:
            self.HIGH_LOW(0.02)
            _ = self.Recieve_Message_From_System(adr, reg)
            self.HIGH_LOW(0.01)
            self.HIGH_LOW(0.01)


    def Send_Message_To_System(self, device_address, register_offset, data):    
        list = [int(str(data), 16)]
        self.bus.write_i2c_block_data(int(str(device_address), 16),
                                      int(str(register_offset), 16),
                                      list)    

    def Recieve_Message_From_System(self, device_address, register_offset):         
        # read a block of 16 bytes from address device_address
        # with offset register_offset
        data = self.bus.read_i2c_block_data(int(str(device_address), 16), 
                                            int(str(register_offset), 16), 16)      
        return data

    def HIGH_LOW(self, wait=0.0002):
        GPIO.output("P8_7", GPIO.HIGH)
        time.sleep(wait)
        GPIO.output("P8_7", GPIO.LOW)

    def Close(self):
        pass

    def Map(self, msg):
        """ consume (msg) a string in the form ADR/REG/DATA and 
        translate to I2C Message """
        if msg == 'reset':
            self.reset()
        elif msg == 'start':
            self.start()
        else:
            self.Process_Message(msg)

    def reset(self):
        self.Send_Message_To_System("w/60/26/04")        

    def start(self):
        print("System Started")
