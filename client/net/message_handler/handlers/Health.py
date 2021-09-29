from .base import MessageHandler
from client.net.server_event import ServerEvent
from client.local import core
from protocol import messages


class HealthHandler(MessageHandler):
    handled_message = messages.HealthUpdateResponse
    response_message = None

    def handle_message(self):
        health_info = self.message.data.data
        core.instance.messenger.send(
            ServerEvent.HEALTH_CHANGED,
            sentArgs=[health_info],
        )
