from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task import Task
from panda3d.core import NetDatagram

import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class SkirmishLocalUpdater:
    """
    Responsible for continuous reading and handling the data sent from the server.
    The data concerns only the actual skirmish gameplay, such as player positions,
    rotations, health points.
    """
    def __init__(self,  manager, skirmish):
        self.manager = manager
        self.skirmish = skirmish
        self.data_handler_mapping = {
            Message.POS_HPR: self.update_pos_hpr,
            Message.NEW_PLAYER: self.update_new_player,
            Message.DISCONNECTION: self.update_disconnection,
            Message.HEALTH: self.update_health,
            Message.CHAT_MSG: self.update_chat,
            Message.IS_MOVING: self.update_is_moving
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
            self.skirmish.world.update_player_pos_hpr(id_, x, y, z, h, p, r)

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
        self.skirmish.create_other_player(id_, class_number, name, health, x, y, z, h, p, r)

    def update_disconnection(self, datagram, iterator):
        """
        Removes the disconnected player from the skirmish.
        """
        id_ = iterator.get_uint8()
        if self.skirmish.player.target is not None and self.skirmish.player.target.id == id_:
            self.skirmish.player.target = None
        self.skirmish.remove_player(id_)

    def update_health(self, datagram, iterator):
        """
        Updates healths points of each player specified in the datagram.
        """
        while iterator.get_remaining_size() > 0:
            id_ = iterator.get_uint8()
            health = iterator.get_uint8()
            player = self.skirmish.get_player_by_id(id_)
            if player is not None:
                player.health = health
            # Check if the message concerns this client's character.
            if self.skirmish.player.id == id_:
                self.skirmish.player.health = health

    def update_chat(self, datagram, iterator):
        """
        Reads the player name and his message from the datagram. Calls the interface method responsible
        for displaying new message.
        """
        name = iterator.get_string()
        message = iterator.get_string()
        self.skirmish.interface.submodules[3].add_message(name, message)

    def update_is_moving(self, datagram, iterator):
        """
        Reads the player's id and information whether they're moving.
        """
        id_ = iterator.get_uint8()
        is_moving = iterator.get_uint8()
        player = self.skirmish.get_player_by_id(id_)
        if player is None:
            return
        player.loop('idle') if is_moving == 0 else player.loop('run')

