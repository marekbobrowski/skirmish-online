from .base import MessageHandler
from protocol import messages, domain


class AnimationHandler(MessageHandler):
    handled_message = messages.AnimationRequest
    response_message = None

    def handle_message(self):
        pass
