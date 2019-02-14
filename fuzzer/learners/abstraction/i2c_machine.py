import time
import abc
import socket

from pylstar.tools.Decorators import PylstarLogger
from pylstar.KnowledgeBase import KnowledgeBase
from pylstar.tools.Decorators import PylstarLogger
from pylstar.ActiveKnowledgeBase import ActiveKnowledgeBase
from pylstar.Letter import Letter, EmptyLetter
from pylstar.Word import Word

@PylstarLogger
class I2CMachineKnowledgeBase(ActiveKnowledgeBase):
    def __init__(self, target_host, target_port, timeout=5):
        super(I2CMachineKnowledgeBase, self).__init__()
        self.target_host = target_host
        self.target_port = target_port
        self.timeout = timeout

    def start_target(self):
        pass

    def stop_target(self):
        pass

    def submit_word(self, word):
        self._logger.debug("Submiting word '{}' to the network target".format(word))
        output_letters = []

        s = socket.socket()
        # Reuse the connection
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(self.timeout)
        s.connect((self.target_host, self.target_port))
        try:
            output_letters = [self._submit_letter(s, letter) for letter in word.letters]
        finally:
            s.close()
        return Word(letters=output_letters)

    def _submit_letter(self, s, letter):
        output_letter = EmptyLetter()
        try:
            to_send = ''.join([symbol for symbol in letter.symbols])
            output_letter = Letter(self._send_and_receive(s, to_send))
        except Exception as e:
            self._logger.error(e)

        return output_letter

    def _send_and_receive(self, s, data):
        """ this is where we have to socket data to the raspberry pi, 
            and start the digitizer by spawning a child process (subprocess.Popen()) """
        s.sendall(data.encode())
        time.sleep(0.1)
        return s.recv(1024).strip()














'''
    def submit_word(self, word):
        self._logger.debug("Submiting word '{}' to the network target".format(word))
        output_letters = []

        s = socket.socket()
        # Reuse the connection
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.settimeout(self.timeout)
        s.connect((self.target_host, self.target_port))
        try:
            output_letters = [self._submit_letter(s, letter) for letter in word.letters]
        finally:
            s.close()
        return Word(letters=output_letters)

    def _submit_letter(self, s, letter):
        output_letter = EmptyLetter()
        try:
            to_send = ''.join([symbol for symbol in letter.symbols])
            output_letter = Letter(self._send_and_receive(s, to_send))
        except Exception:
            self._logger.error(e)

        return output_letter

    def _send_and_receive(self, s, data):
        s.sendall(data)
        time.sleep(0.1)
        return s.recv(1024).strip()

'''
