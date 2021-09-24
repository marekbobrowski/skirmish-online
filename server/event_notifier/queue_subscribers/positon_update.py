from protocol import messages, domain
import json


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
        self.event_notifier.notify(
            messages.PosHPRResponse.build(data),
        )

    def run(self):
        """
        Creates thread subscribed to the channel
        """
        self.event_notifier.session.player_cache.subscribe(self)
