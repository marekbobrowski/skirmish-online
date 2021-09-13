from direct.distributed.PyDatagram import PyDatagram
import sys
import os

sys.path.append(os.path.abspath(os.path.join("..")))
from protocol.message import Message
from threading import Thread
from . import cooldown_countdown
from panda3d.core import Vec3
from random import randint


class SpellHandler:
    def __init__(self, server):
        self.server = server

    def handle_action(self, datagram, iterator):
        connection = datagram.get_connection()
        player = self.server.find_player_by_connection(connection)
        action_id = iterator.get_uint8()
        targets = self.get_near_targets(player)
        self.perform_test_action(player, targets, action_id)

    def get_near_targets(self, player):
        targets = []
        for other_player in self.server.active_connections:
            if (
                other_player.joined_game
                and other_player is not player
                and (other_player.get_vec3_pos() - player.get_vec3_pos()).length() < 0.5
            ):
                targets.append(other_player)
        return targets

    def perform_test_action(self, source, targets, action_id):
        if source.cooldowns[action_id] != 0:
            return
        temp_cooldown = 5

        # # trigger cooldown count down first
        # Thread(target=cooldown_countdown.cooldown_countdown,
        #        daemon=True,
        #        args=(source, action_id, temp_cooldown)).start()

        hp_change = -1 * randint(1, 10)

        for target in targets:
            target.health += hp_change
            if target.health <= 0:
                target.health = 0

        # action_datagram = PyDatagram()
        # action_datagram.add_uint8(Message.ACTION)
        # action_datagram.add_uint8(source.id)
        # action_datagram.add_uint8(action_id)
        # action_datagram.add_uint8(temp_cooldown)  # temporarily hard-coded 5 sec cooldown

        combat_data = PyDatagram()
        combat_data.add_uint8(Message.COMBAT_DATA)
        combat_data.add_uint8(action_id)
        combat_data.add_int8(hp_change)
        combat_data.add_uint8(source.id)

        for target in targets:
            combat_data.add_uint8(target.id)

        health_datagram = PyDatagram()
        health_datagram.add_uint8(Message.HEALTH)

        for target in targets:
            health_datagram.add_uint8(target.id)
            health_datagram.add_uint8(target.health)

        # animation_datagram = PyDatagram()
        # animation_datagram.add_uint8(Message.ANIMATION)
        # animation_datagram.add_uint8(source.id)
        # animation_datagram.add_string('attack')
        # animation_datagram.add_uint8(0)

        for player in self.server.active_connections:
            if player.joined_game:
                # self.server.writer.send(action_datagram, player.connection)
                self.server.writer.send(health_datagram, player.connection)
                self.server.writer.send(combat_data, player.connection)
                # self.server.writer.send(animation_datagram, player.connection)
