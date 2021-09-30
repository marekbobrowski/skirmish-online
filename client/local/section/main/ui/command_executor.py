from client.local import core
from client.event import Event


class CommandExecutor:
    def __init__(self, command):
        self.command = command

    def __call__(self):
        self.parse()

    def parse(self):
        # for now we only send messages to server
        self.send_msg_to_server(self.command)

    def send_msg_to_server(self, msg):
        core.instance.messenger.send(
            event=Event.COMMAND_TO_SERVER_ENTERED, sentArgs=[msg]
        )
