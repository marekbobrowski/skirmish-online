from protocol import messages
from .base import SubNotifierBase
from server.event.event import Event
from datetime import datetime

import logging
import json

log = logging.getLogger(__name__)


class TextMessageNotifier(SubNotifierBase):
    MESSAGE = messages.TextMessageResponse
    EVENT = Event.TEXT_MESSAGE

    def __call__(self, message):
        data = json.loads(message)
        if data.get("send_dtime", None):
            data["send_dtime"] = datetime.fromtimestamp(data["send_dtime"])

        self.event_notifier.notify(
            messages.TextMessageResponse.build(data),
        )

