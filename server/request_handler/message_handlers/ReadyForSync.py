from .base import MessageHandler
from protocol import messages
from ... import config


class ReadyForSyncHandler(MessageHandler):
    handled_message = messages.ReadyForSyncRequest
    response_message = messages.TextMessageResponse

    def handle_message(self):
        pass

    def build_response(self) -> messages.TextMessageResponse:
        message = messages.TextMessageResponse.build(
            [
                [None, None, config.welcome_msg],
            ],
        )

        return message
