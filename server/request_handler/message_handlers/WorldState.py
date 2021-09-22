from .base import MessageHandler
from protocol import messages, domain
from ... import config
from ...storage.domain import Player
import random


class WorldStateHandler(MessageHandler):
    handled_message = messages.WorldStateRequest
    response_message = messages.WorldStateResponse

    def handle_message(self):
        pass

    def build_response(self) -> messages.WelcomeMessageResponse:
        # TODO
        self.session.for_player(random.randrange(0, 10))
        other_players = self.session.player_cache.other_players()
        message = messages.WorldStateResponse.build(
            [
                self.session.player,
                other_players,
            ],
        )
        return message
