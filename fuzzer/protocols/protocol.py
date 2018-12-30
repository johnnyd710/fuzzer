from abc import ABC, abstractmethod

class Protocol(ABC):
    def __init__(self):
        '''
        initialize with 
        '''
        self.identifier = ''
        self.data = ''
        super().__init__()

    def __str__(self):
        print(self.identifier)
        print(self.data)

    @abstractmethod
    def flip_rand_bit(self):
        pass

    @abstractmethod
    def randomize_data(self):
        pass
    