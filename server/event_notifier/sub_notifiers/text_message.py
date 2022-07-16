from protocol import messages, domain
import json
from datetime import datetime
import logging


log = logging.getLogger(__name__)


class TextMessageNotifier:
    def __init__(self, event_notifier):
        """
        TextMessageSubscriber notifies user
        with new text messages
        """
        self.event_notifier = event_notifier

    def __call__(self, message):
        """
        Subscribed method, prepares response and pushes it
        """
        data = json.loads(message)
        if data.get("send_dtime", None):
            data["send_dtime"] = datetime.fromtimestamp(data["send_dtime"])

        self.event_notifier.notify(
            messages.TextMessageResponse.build(data),
        )

    def start_listening(self):
        """
        Creates thread subscribed to the channel
        """
        self.event_notifier.session.text_message_cache.subscribe(self)
