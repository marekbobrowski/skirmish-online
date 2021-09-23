from protocol import messages
import json


class SpellSubscriber:
    def __init__(self, event_notifier):
        """
        AnimationUpdateSubscriber notifies user of animation changes
        for all other users
        """
        self.event_notifier = event_notifier

    def __call__(self, message):
        """
        Subscribed method, prepares response and pushes it
        """
        data = json.loads(message["data"])

        self.event_notifier.notify(
             messages.CombatDataResponse.build(data),
        )

    def run(self):
        """
        Creates thread subscribed to the channel
        """
        self.event_notifier.session.spell_cache.subscribe(self)
