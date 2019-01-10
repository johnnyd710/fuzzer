'''
I2C class converts msg identifier in the Data.data dict to its
i2c representation.
Also has extra functionality for abstracting results into 
a grammar or "rule set"
'''

import random

class I2C_Msg:
    def __init__(self):
        # fill with random bits
        self.adr = range(256)
        self.reg = range(256)

    def out(self, a, r):
        return 'ADR:' + str(self.adr[a]) + 'REG:' + str(self.reg[r])

    def valid(self):
        """ return valid addresses/registers """
        pass

    def flip_rand_bit(self):
        pass

    def randomize_data(self):
        pass

    def get_json(self):
        # there is no need for json???
        pass