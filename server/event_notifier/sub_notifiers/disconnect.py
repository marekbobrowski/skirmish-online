from protocol import messages
from .base import SubNotifierBase
from server.event.event import Event

import json
import logging

log = logging.getLogger(__name__)


class DisconnectionNotifier(SubNotifierBase):
    MESSAGE = messages.DisconnectResponse
    EVENT = Event.DISCONNECTION

    def __call__(self, message):
        data = json.loads(message)
        data = messages.DisconnectResponse.build(data)
        self.event_notifier.notify(data)
        self.event_notifier.session.player_position_cache.remove_positions([data.data.id])

