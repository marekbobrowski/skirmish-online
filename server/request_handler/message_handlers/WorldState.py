from .base import MessageHandler
from protocol import messages, domain
from ... import config
from ...storage.domain import Player


class WorldStateHandler(MessageHandler):
    handled_message = messages.WorldStateRequest
    response_message = messages.WorldStateResponse

    def handle_message(self):
        pass

    def build_response(self) -> messages.WelcomeMessageResponse:
        # TODO
        self.session.for_player(0)
        message = messages.WorldStateResponse.build(
            [
                [
                    self.session.player.id,
                    self.session.player.name,
                    self.session.player.health,
                    self.session.player.model,
                    self.session.player.animation,
                    self.session.player.weapon,
                    self.session.player.x,
                    self.session.player.y,
                    self.session.player.z,
                    self.session.player.h,
                    self.session.player.p,
                    self.session.player.r,
                ],
            ],
        )
        return message
