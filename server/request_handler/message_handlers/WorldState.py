from .base import MessageHandler
from protocol import messages, domain
from ... import config


class WorldStateHandler(MessageHandler):
    handled_message = messages.WorldStateRequest
    response_message = messages.WorldStateResponse

    def handle_message(self):
        pass

    def build_response(self) -> messages.WelcomeMessageResponse:
        message = messages.WorldStateResponse.build(
            [
                [
                    0,
                    "name",
                    50,
                    1,
                    "stand",
                    1,
                    -3,
                    -5,
                    1,
                    120,
                    0,
                    0,
                ],
            ],
        )
        return message
