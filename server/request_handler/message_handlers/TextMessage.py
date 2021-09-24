from .base import MessageHandler
from ...storage.domain import TextMessage
from protocol import messages
from datetime import datetime


class TextMessageHandler(MessageHandler):
    handled_message = messages.TextMessageRequest
    response_message = None

    def handle_message(self):
        """
        Distrubute text message
        """
        text_message_data = self.message.data
        text_message = TextMessage(
            player_name=self.session.player.name,
            send_dtime=datetime.now(),
            message=text_message_data,
        )
        self.session.text_message_cache.publish_text_message(text_message)
