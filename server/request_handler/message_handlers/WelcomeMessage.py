from .base import MessageHandler
from protocol import messages, domain
from ... import config


class WelcomeMessageHandler(MessageHandler):
    handled_message = messages.WelcomeMessageRequest
    response_message = messages.WelcomeMessageResponse

    def handle_message(self):
        pass

    def build_response(self) -> messages.WelcomeMessageResponse:
        message = messages.WelcomeMessageResponse(
            [
                domain.LongMessage(config.welcome_msg),
            ]
        )
        return message
