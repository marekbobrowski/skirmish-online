from protocol import messages
from .base import SubNotifierBase
from server.event.event import Event
from ...storage.domain import PlayerPositionUpdate

import logging

log = logging.getLogger(__name__)


class PositionUpdateNotifier(SubNotifierBase):
    MESSAGE = messages.PosHPRResponse
    EVENT = Event.POSITION_UPDATED
    DROP_FOR_SELF = True

    def update_cache(self, data):
        self.event_notifier.session.player_position_cache.update_position(data)
