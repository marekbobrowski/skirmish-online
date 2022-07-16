from ..domain import TextMessage
import json
import dataclasses
import logging
from server.event.event_user import EventUser
from server.event.event import Event


log = logging.getLogger(__name__)


class TextMessageCache(EventUser):

    def __init__(self, session):
        super().__init__()
        self.session = session

    def publish_text_message(self, text_message: TextMessage):
        """
        Broadcasts a spell.
        """
        message_dict = dataclasses.asdict(text_message)
        if message_dict.get("send_dtime", None):
            message_dict["send_dtime"] = message_dict["send_dtime"].timestamp()
        data = json.dumps(message_dict)

        self.send_event(
            event=Event.TEXT_MESSAGE,
            prepared_data=data,
        )

