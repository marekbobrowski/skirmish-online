from .base import MessageHandler
from client.net.server_event import ServerEvent
from client.local import core
from protocol import messages


class CombatDataHandler(MessageHandler):
    handled_message = messages.CombatDataResponse
    response_message = None

    def handle_message(self):
        data = self.message.data
        core.instance.messenger.send(
            ServerEvent.RECEIVED_COMBAT_DATA,
            sentArgs=[data.spell, data.hp_change, data.source, data.targets.data],
        )
