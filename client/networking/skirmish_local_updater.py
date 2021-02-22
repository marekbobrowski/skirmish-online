from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task import Task
from panda3d.core import NetDatagram
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class SkirmishLocalUpdater:
    def __init__(self,  skirmish, manager):
        self.manager = manager
        self.skirmish = skirmish

    """
    Continuously attempts to catch data sent by the server.
    """
    def listen_for_updates(self, task):
        if self.manager.connected:
            if self.manager.reader.data_available():
                datagram = NetDatagram()
                iterator = PyDatagramIterator(datagram)
                if self.manager.reader.get_data(datagram):
                    self.process_updates(datagram, iterator)
            return Task.cont
        else:
            return Task.done

    def process_updates(self, datagram, iterator):
        packet_type = iterator.get_uint8()
        if packet_type == Message.POS_HPR:
            self.update_pos_hpr(datagram, iterator)
        elif packet_type == Message.NEW_PLAYER:
            self.update_new_player(datagram, iterator)
        elif packet_type == Message.DISCONNECTION:
            self.update_disconnection(datagram, iterator)
        elif packet_type == Message.HEALTH:
            self.update_health(datagram, iterator)

    def update_pos_hpr(self, datagram, iterator):
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
        self.skirmish.create_other_player(class_number, id_, name, health, x, y, z, h, p, r)

    def update_disconnection(self, datagram, iterator):
        id_ = iterator.get_uint8()
        if self.skirmish.player.target is not None and self.skirmish.player.target.id == id_:
            self.skirmish.player.target = None
        self.skirmish.remove_player(id_)

    def update_health(self, datagram, iterator):
        id_ = iterator.get_uint8()
        health = iterator.get_uint8()
        player = self.skirmish.get_player_by_id(id_)
        if player is not None:
            player.health = health
            return
        if self.skirmish.player.id == id_:
            self.skirmish.player.health = health

