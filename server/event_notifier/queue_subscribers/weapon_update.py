from protocol import messages, domain
import json
import logging

log = logging.getLogger(__name__)


class WeaponUpdateSubscriber:
    def __init__(self, event_notifier):
        """
        NameUpdateSubscriber notifies user
        with name changes
        """
        self.event_notifier = event_notifier

    def __call__(self, message):
        """
        Subscribed method, prepares response and pushes it
        """
        data = json.loads(message["data"])

        self.event_notifier.notify(
            messages.WeaponUpdateMessage.build(data),
        )

    def run(self):
        """
        Creates thread subscribed to the channel
        """
        self.event_notifier.session.player_cache.subscribe_weapon_update(self)
