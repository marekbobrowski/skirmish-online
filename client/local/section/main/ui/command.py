from client.local import core
from client.net.server_event import ServerEvent
from client.local.client_event import ClientEvent


def parse(command):
    words = command.split()
    command_mapping.get(words[0], send_msg_to_server)(command, words)


def send_msg_to_server(msg, words):
    core.instance.messenger.send(event=ClientEvent.COMMAND_TO_SERVER, sentArgs=[msg])


def set_volume(amt):
    pass


def toggle_combat_log():
    pass


core.instance.accept(ClientEvent.COMMAND, parse)


class Command:
    MESSAGE_TO_SERVER = 0
    SET_VOLUME = "/setvolume"
    TOGGLE_COMBAT_LOG = "/cltoggle"


command_mapping = {Command.MESSAGE_TO_SERVER: send_msg_to_server}
