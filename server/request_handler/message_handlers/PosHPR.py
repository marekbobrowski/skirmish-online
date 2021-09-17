from .base import MessageHandler
from protocol import messages, domain


class PosHPRHandler(MessageHandler):
    handled_message = messages.PosHPRRequest
    response_message = None

    def handle_message(self):
        player = self.server.find_player_by_connection(self.connection)
        player_pos = self.message.data[0]
        player.set_pos_hpr(
            player_pos.x,
            player_pos.y,
            player_pos.z,
            player_pos.h,
            player_pos.p,
            player_pos.r,
        )
