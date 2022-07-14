from protocol import messages, domain
import json
import logging

log = logging.getLogger(__name__)


class DisconnectSubscriber:
    def __init__(self, event_notifier):
        """
        HealthUpdateSubscriber notifies user
        with health changes
        """
        self.event_notifier = event_notifier

    def __call__(self, message):
        """
        Subscribed method, prepares response and pushes it
        """
        data = json.loads(message["data"])
        data = messages.DisconnectResponse.build(data)

        self.event_notifier.notify(data)
        self.event_notifier.session.player_position_cache.remove_positions([data.data.id])

    def run(self):
        """
        Creates thread subscribed to the channel
        """
        self.event_notifier.session.player_cache.subscribe_disconnect(self)
