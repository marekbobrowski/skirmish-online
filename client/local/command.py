from local import core
from event import Event


def parse(command):
    words = command.split()
    command_mapping.get(words[0], send_msg_to_server)(command, words)


def send_msg_to_server(msg, words):
    core.instance.messenger.send(event=Event.TXT_MSG_TO_SERVER_TYPED, sentArgs=[msg])


def set_volume(amt):
    pass


def toggle_combat_log():
    pass


core.instance.accept(Event.COMMAND_TYPED, parse)


class Command:
    MESSAGE_TO_SERVER = 0
    SET_VOLUME = '/setvolume'
    TOGGLE_COMBAT_LOG = '/cltoggle'


command_mapping = {
    Command.MESSAGE_TO_SERVER: send_msg_to_server
}




