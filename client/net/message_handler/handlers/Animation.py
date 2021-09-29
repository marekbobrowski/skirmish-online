from .base import MessageHandler
from client.net.server_event import ServerEvent
from client.local import core
from protocol import messages


class AnimationMessageHandler(MessageHandler):
    handled_message = messages.AnimationResponse
    response_message = None

    def handle_message(self):
        data = self.message.data
        id_, anim_name, loop = data.id, data.animation_name, data.loop
        core.instance.messenger.send(
            ServerEvent.PLAYER_CHANGED_ANIMATION, sentArgs=[id_, anim_name, loop]
        )
