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
        data = json.loads(message["data"])
        event_dtime = datetime.fromtimestamp(data.pop("event_dtime"))

        log.info(
            f"delay: {(datetime.now() - event_dtime).total_seconds() * 1000}, notified {self.event_notifier.session.player.id} about {data['id']}"
        )

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
