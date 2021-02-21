from direct.distributed.PyDatagram import PyDatagram
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class ActionHandler:
    def __init__(self, server):
        self.server = server

    def handle_action(self, datagram, iterator):
        connection = datagram.get_connection()
        player = self.server.find_player_by_connection(connection)
        action_code = iterator.get_uint8()
        target = self.server.find_player_by_id(iterator.get_uint8())
        self.perform_test_action(player, target)

    def perform_test_action(self, source, target):
        target.health -= 10
        if target.health <= 0:
            target.health = 0
        datagram = PyDatagram()
        datagram.add_uint8(Message.HEALTH)
        datagram.add_uint8(target.id)
        datagram.add_uint8(target.health)

        for player in self.server.active_connections:
            if player.joined_game:
                self.server.writer.send(datagram, player.connection)


