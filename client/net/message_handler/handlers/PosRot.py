from .base import MessageHandler
from client.net.server_event import ServerEvent
from client.local import core
from protocol import messages

import logging


log = logging.getLogger(__name__)


class PosRotHandler(MessageHandler):
    handled_message = messages.PosHPRResponse
    response_message = None

    def handle_message(self):
        data = self.message.data
        core.instance.messenger.send(
            ServerEvent.PLAYER_CHANGED_POS_HPR,
            sentArgs=[data.id, data.x, data.y, data.z, data.h, data.p, data.r],
        )
