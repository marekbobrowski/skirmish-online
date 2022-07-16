from protocol.messages.base import Message
from server.event.event_user import EventUser
from server.event.event import Event
import json
import logging

log = logging.getLogger(__name__)


class SubNotifierBase(EventUser):
    EVENT: Event = None
    MESSAGE: Message = None

    def __init__(self, event_notifier):
        """
        Notifies user about some game event.
        """
        super().__init__()
        self.event_notifier = event_notifier

    def __call__(self, message):
        """
        Handle event by notifying user.
        """
        data = json.loads(message)

        self.event_notifier.notify(
            self.MESSAGE.build(data),
        )

    def start_listening(self):
        """
        Start listening for event.
        """
        self.accept_event(event=self.EVENT,
                          handler=self)
