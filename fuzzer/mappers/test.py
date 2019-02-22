from redis import Redis


class Mapper_Test():

    def __init__(self):
        """ vocab should be a list of strings formatted as follows:  
        [ADR1/REG1/DATA1, ADR1/REG1/DATA2 ... etc.] 
        representing the available input space"""
        super().__init__()
        self.r = Redis(host='localhost', port=6379, db=0)

    def Send_Message_To_System(self, msg):    
        self.r.publish('Comms',msg)

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
            self.Send_Message_To_System(msg)

    def reset(self):
        self.r.publish('Comms','reset')

    def start(self):
        self.r.publish('Comms','start')
