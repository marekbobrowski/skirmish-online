from protocol import messages, domain
from ...storage.domain import PlayerPositionUpdate
import json
import logging
from datetime import datetime


log = logging.getLogger(__name__)


class PositionUpdateSubscriber:
    def __init__(self, event_notifier):
        """
        PositionUpdateSubscriber notifies user of position changes
        for all other users
        """
        self.event_notifier = event_notifier

    def __call__(self, message):
        """
        Subscribed method, prepares response and pushes it
        """
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

    def run(self):
        """
        Creates thread subscribed to the channel
        """
        self.event_notifier.session.player_cache.subscribe(self)
