from protocol import messages, domain
import json
import logging

log = logging.getLogger(__name__)


class ManaUpdateNotifier:
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
        data = json.loads(message)
        self.event_notifier.notify(
            messages.ManaUpdateResponse.build(data),
        )

    def start_listening(self):
        """
        Creates thread subscribed to the channel
        """
        self.event_notifier.session.player_cache.subscribe_mana_update(self)
