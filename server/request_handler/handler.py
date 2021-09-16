from direct.distributed.PyDatagramIterator import PyDatagramIterator
from protocol.parser import MessageParser


class Handler:
    def __init__(self, server):
        self.server = server
        self.message_parser = MessageParser()

    def handle_data(self, datagram):
        iterator = PyDatagramIterator(datagram)
        message = self.message_parser(iterator)
        self.handle_message(message)

    def handle_message(self, message):
        pass
