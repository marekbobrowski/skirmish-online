from protocol import messages, domain
from ...storage.domain import PlayerPositionUpdate
import json
import logging

log = logging.getLogger(__name__)


class NewPlayerSubscriber:
    def __init__(self, event_notifier):
        """
        NewPlayerSubscriber notifies user
        with new users
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

    def run(self):
        """
        Creates thread subscribed to the channel
        """
        self.event_notifier.session.player_cache.subscribe_new_players(self)
