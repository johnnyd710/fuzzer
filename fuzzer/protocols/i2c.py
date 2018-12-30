from protocol import Protocol
import random

class I2C_Msg(Protocol):
    def __init__(self):
        # fill with random bits
        self.address = ''
        self.register = ''
        self.data = ''
        super().__init__(self, self.address + self.register, self.data)

    def flip_rand_bit(self):
        pass

    def randomize_data(self):
        pass

    def get_json(self):
        # there is no need for json???
        pass