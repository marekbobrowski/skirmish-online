from direct.distributed.PyDatagram import PyDatagram
from protocol.message import Message
from threading import Thread
from . import cooldown_countdown
from panda3d.core import Vec3
from . import config
from random import randint


class SpellHandler:
    def __init__(self, server):
        self.server = server

    def handle_action(self, datagram, iterator):
        connection = datagram.get_connection()
        player = self.server.find_player_by_connection(connection)
        spell_id = iterator.get_uint8()
        targets = self.get_near_targets(player)
        self.perform_test_action(player, targets, spell_id)

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

    def perform_test_action(self, source, targets, slot_number):
        if source.spell_ids[slot_number] == -1:
            return

        if source.cooldowns[slot_number] != 0:
            return

        # trigger cooldown count down first
        Thread(target=cooldown_countdown.cooldown_countdown,
               daemon=True,
               args=(source, slot_number, config.spell_cooldowns[source.spell_ids[slot_number]])).start()

        hp_change = -1 * randint(5, 10)

        for target in targets:
            target.health += hp_change
            if target.health <= 0:
                target.health = 0

        cooldown_data = PyDatagram()
        cooldown_data.add_uint8(Message.TRIGGER_COOLDOWN)
        cooldown_data.add_uint8(slot_number)

        combat_data = PyDatagram()
        combat_data.add_uint8(Message.COMBAT_DATA)
        combat_data.add_uint8(slot_number)
        combat_data.add_int8(hp_change)
        combat_data.add_uint8(source.id)

        for target in targets:
            combat_data.add_uint8(target.id)

        health_datagram = PyDatagram()
        health_datagram.add_uint8(Message.HEALTH)

        for target in targets:
            health_datagram.add_uint8(target.id)
            health_datagram.add_uint8(target.health)

        animation_datagram = PyDatagram()
        animation_datagram.add_uint8(Message.ANIMATION)
        animation_datagram.add_uint8(source.id)
        animation_datagram.add_string('melee_attack_1')
        animation_datagram.add_uint8(0)

        for player in self.server.active_connections:
            if player.joined_game:
                # self.server.writer.send(action_datagram, player.connection)
                self.server.writer.send(health_datagram, player.connection)
                self.server.writer.send(combat_data, player.connection)
                self.server.writer.send(animation_datagram, player.connection)

        self.server.writer.send(cooldown_data, source.connection)
