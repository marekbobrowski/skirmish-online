from protocol import messages, domain
import json
import logging


log = logging.getLogger(__name__)


class AnimationUpdateSubscriber:
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
        data = json.loads(message)
        self.event_notifier.notify(
            messages.AnimationResponse.build(data),
        )

    def run(self):
        """
        Creates thread subscribed to the channel
        """
        self.event_notifier.session.player_cache.subscribe_animation_update(self)
