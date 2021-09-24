from protocol import messages, domain
import json


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
        data = json.loads(message["data"])
        self.event_notifier.notify(
            messages.NewPlayerResponse.build(data),
        )

    def run(self):
        """
        Creates thread subscribed to the channel
        """
        self.event_notifier.session.player_cache.subscribe_new_players(self)
