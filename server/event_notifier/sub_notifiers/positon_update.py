from protocol import messages
from .base import SubNotifierBase
from server.event.event import Event
from ...storage.domain import PlayerPositionUpdate

import json
import logging

log = logging.getLogger(__name__)


class PositionUpdateNotifier(SubNotifierBase):
    MESSAGE = messages.PosHPRResponse
    EVENT = Event.POSITION_UPDATED

    def __call__(self, message):
        data = json.loads(message)
        if (
            self.event_notifier.session.player is not None
            and data["id"] == self.event_notifier.session.player.id
        ):
            return

        data.pop("event_dtime")

        self.event_notifier.session.player_position_cache.update_position(
            PlayerPositionUpdate(**data),
        )
        self.event_notifier.notify(
            messages.PosHPRResponse.build(data),
        )

