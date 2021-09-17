from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram
from protocol.parser import MessageParser
from protocol.messages import MessageType
from .message_handlers import MessageHandlersBank


class Handler:
    def __init__(self, server):
        self.server = server
        self.message_parser = MessageParser()

    def handle_data(self, datagram):
        iterator = PyDatagramIterator(datagram)
        connection = datagram.get_connection()
        message = self.message_parser(iterator, MessageType.request)
        response = self.handle_message(connection, message)
        self.handle_response(connection, response)

    def handle_response(self, connection, response) -> None:
        if response is None:
            return

        response_datagram = PyDatagram()
        response.dump(response_datagram)
        self.server.writer.send(response_datagram, connection)

    def handle_message(self, connection, message):
        handler = MessageHandlersBank.by_id(message.ID)(
            self.server,
            connection,
            message,
        )
        return handler()
