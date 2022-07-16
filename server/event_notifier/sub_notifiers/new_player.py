from protocol import messages
from .base import SubNotifierBase
from server.event.event import Event
from ...storage.domain import PlayerPositionUpdate

import logging
import json

log = logging.getLogger(__name__)


class NewPlayerNotifier(SubNotifierBase):
    MESSAGE = messages.NewPlayerResponse
    EVENT = Event.NEW_PLAYER_JOINED

    def __call__(self, message):
        data = json.loads(message)

        if (
            self.event_notifier.session.player is not None
            and data["id"] == self.event_notifier.session.player.id
        ):
            return

        self.event_notifier.session.player_position_cache.update_position(
            PlayerPositionUpdate(
                id=data["id"],
                x=data["x"],
                y=data["y"],
                z=data["z"],
                h=data["h"],
                p=data["p"],
                r=data["r"],
            ),
        )
        self.event_notifier.notify(
            messages.NewPlayerResponse.build(data),
        )

