from ..domain import TextMessage
import json
import dataclasses
import logging
from server.event.event_user import EventUser


log = logging.getLogger(__name__)


class TextMessageCache(EventUser):
    TEXT_MESSAGE_CHANNEL = "text_message_"

    def __init__(self, session):
        super().__init__()
        self.session = session

    @classmethod
    def text_message_channel_for_session(cls, session_id):
        """
        Creates a unique channel name for the session.
        """
        return f"{cls.TEXT_MESSAGE_CHANNEL}{session_id}"

    def publish_text_message(self, text_message: TextMessage):
        """
        Broadcasts a spell.
        """
        message_dict = dataclasses.asdict(text_message)
        if message_dict.get("send_dtime", None):
            message_dict["send_dtime"] = message_dict["send_dtime"].timestamp()
        data = json.dumps(message_dict)

        for session_id in self.session.cache.get_all_sessions():
            self.session.redis.publish(
                self.text_message_channel_for_session(session_id),
                data,
            )

    def subscribe(self, subscriber):
        """
        Creates a thread that will subscribe to text messages
        """
        p = self.session.redis.pubsub()
        p.subscribe(
            **{self.text_message_channel_for_session(self.session.id): subscriber}
        )
        thread = p.run_in_thread(sleep_time=0.001)
        self.listening_threads.append(thread)
        return thread
