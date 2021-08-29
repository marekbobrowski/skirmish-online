from direct.distributed.PyDatagram import PyDatagram
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message
from threading import Thread
import cooldown_countdown


class ActionHandler:
    def __init__(self, server):
        self.server = server

    def handle_action(self, datagram, iterator):
        connection = datagram.get_connection()
        player = self.server.find_player_by_connection(connection)
        action_id = iterator.get_uint8()
        target = self.server.find_player_by_id(iterator.get_uint8())
        self.perform_test_action(player, target, action_id)

    def perform_test_action(self, source, target, action_id):
        if source.cooldowns[action_id] != 0:
            return

        temp_cooldown = 5

        # trigger cooldown count down first
        Thread(target=cooldown_countdown.cooldown_countdown,
               daemon=True,
               args=(source, action_id, temp_cooldown)).start()

        target.health -= 10
        if target.health <= 0:
            target.health = 0

        action_datagram = PyDatagram()
        action_datagram.add_uint8(Message.ACTION)
        action_datagram.add_uint8(source.id)
        action_datagram.add_uint8(action_id)
        action_datagram.add_uint8(temp_cooldown)  # temporarily hard-coded 5 sec cooldown

        health_datagram = PyDatagram()
        health_datagram.add_uint8(Message.HEALTH)
        health_datagram.add_uint8(target.id)
        health_datagram.add_uint8(target.health)

        animation_datagram = PyDatagram()
        animation_datagram.add_uint8(Message.ANIMATION)
        animation_datagram.add_uint8(source.id)
        animation_datagram.add_string('attack')
        animation_datagram.add_uint8(0)

        for player in self.server.active_connections:
            if player.joined_game:
                self.server.writer.send(action_datagram, player.connection)
                self.server.writer.send(health_datagram, player.connection)
                self.server.writer.send(animation_datagram, player.connection)




