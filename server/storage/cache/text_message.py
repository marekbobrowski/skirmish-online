from ..domain import TextMessage
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
        self.send_event(
            event=Event.TEXT_MESSAGE,
            prepared_data=text_message,
        )

