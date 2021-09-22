from .base import MessageHandler
from protocol import messages, domain
import logging


log = logging.getLogger(__name__)


class AnimationHandler(MessageHandler):
    handled_message = messages.AnimationRequest
    response_message = None

    def handle_message(self):
        animation_data = self.message.data[0]
        self.session.set_animation(animation_data)
