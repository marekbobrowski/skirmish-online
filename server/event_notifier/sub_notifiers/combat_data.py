from protocol import messages, domain
import json
import logging

log = logging.getLogger(__name__)


class CombatDataNotifier:
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
        data = json.loads(message)

        self.event_notifier.notify(
            messages.CombatDataResponse.build(data),
        )

    def start_listening(self):
        """
        Creates thread subscribed to the channel
        """
        self.event_notifier.session.spell_cache.subscribe_for_combat_data(self)
