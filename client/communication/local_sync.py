from local import core
from event import Event

import sys
import os

from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.interval.IntervalGlobal import *
from direct.task import Task
from panda3d.core import NetDatagram

sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class LocalSync:
    """
    Responsible for continuous reading and handling the data sent from the server.
    The data concerns only the actual skirmish gameplay, such as player positions,
    rotations, health points.
    """
    def __init__(self, manager, world):
        self.console = None
        self.manager = manager
        self.world = world
        self.data_handler_mapping = {
            Message.POS_HPR: self.update_pos_hpr,
            Message.NEW_PLAYER: self.update_new_player,
            Message.DISCONNECTION: self.update_disconnection,
            Message.HEALTH: self.update_health,
            Message.TEXT_MSG: self.update_chat,
            Message.ANIMATION: self.update_animation,
            Message.ACTION: self.update_action,
            Message.SET_NAME: self.update_name
        }

    def listen_for_updates(self, task):
        """
        Continuously attempts to catch data sent by the server. If succeeds, sends it further.
        """
        if self.manager.reader.data_available():
            datagram = NetDatagram()
            iterator = PyDatagramIterator(datagram)
            if self.manager.reader.get_data(datagram):
                self.process_updates(datagram, iterator)
        return Task.cont

    def process_updates(self, datagram, iterator):
        """
        Reads the first unsigned integer of the packet to recognize the message type and,
        depending on it's value, sends the packet to the proper handler.
        """
        packet_type = iterator.get_uint8()
        if packet_type not in self.data_handler_mapping:
            return
        self.data_handler_mapping.get(packet_type)(datagram, iterator)

    def update_pos_hpr(self, datagram, iterator):
        """
        Reads and updates the positions and rotations of each player (except this one) in the game.
        """
        while iterator.get_remaining_size() > 0:
            id_ = iterator.get_uint8()
            x = iterator.get_float64()
            y = iterator.get_float64()
            z = iterator.get_float64()
            h = iterator.get_float64()
            p = iterator.get_float64()
            r = iterator.get_float64()
            self.world.update_player_pos_hpr(id_, x, y, z, h, p, r)

    def update_new_player(self, datagram, iterator):
        """
        Creates a new player with given id, name, position etc and places them in the world.
        """
        id_ = iterator.get_uint8()
        name = iterator.get_string()
        class_number = iterator.get_uint8()
        health = iterator.get_uint8()
        x = iterator.get_float64()
        y = iterator.get_float64()
        z = iterator.get_float64()
        h = iterator.get_float64()
        p = iterator.get_float64()
        r = iterator.get_float64()
        player = self.world.create_other_player(id_, class_number, name, health, x, y, z, h, p, r)
        core.instance.messenger.send('player-base-updated')
        core.instance.messenger.send(event=Event.PLAYER_JOINED, sentArgs=[player])

    def update_disconnection(self, datagram, iterator):
        """
        Removes the disconnected player from the skirmish.
        """
        id_ = iterator.get_uint8()
        if self.world.player.target is not None and self.world.player.target.id == id_:
            self.world.player.target = None
        self.world.remove_player(id_)

    def update_health(self, datagram, iterator):
        """
        Updates healths points of each player specified in the datagram.
        """
        while iterator.get_remaining_size() > 0:
            id_ = iterator.get_uint8()
            health = iterator.get_uint8()
            player = self.world.get_any_player_by_id(id_)
            if player is not None:
                player.health = health
                core.instance.messenger.send(event=Event.HEALTH_CHANGED, sentArgs=[player])

    def update_chat(self, datagram, iterator):
        """
        Reads the player name and his message from the datagram. Calls the interface method responsible
        for displaying new message.
        """
        name = iterator.get_string()
        time = iterator.get_string()
        message = iterator.get_string()
        self.console.add_lines([f"[{time}] {name}: {message}"])
        self.console.update_view()

    def update_animation(self, datagram, iterator):
        """
        Reads the player's id and information about their animation.
        """
        id_ = iterator.get_uint8()
        animation = iterator.get_string()
        loop = iterator.get_uint8()
        player = self.world.get_other_player_by_id(id_)
        if player is None:
            if self.world.player.id != id_:
                return
            else:
                player = self.world.player
        if loop:
            pass
            player.character.loop(animation)
        else:
            pass
            player.character.play(animation)

    def update_action(self, datagram, iterator):
        id_ = iterator.get_uint8()
        action_id = iterator.get_uint8()
        cd_time = iterator.get_uint8()
        print('Player with id ' + str(id_) + ' used action: ' + str(action_id) + 'and dealt x dmg.')
        if id_ == self.world.player.id:
            self.world.abilities.trigger_cooldown(action_id, cd_time)

    def update_name(self, datagram, iterator):
        id_ = iterator.get_uint8()
        new_name = iterator.get_string()
        player = self.world.get_any_player_by_id(id_)
        if player is not None:
            player.name = new_name
            core.instance.messenger.send(event=Event.NAME_CHANGED, sentArgs=[player])
