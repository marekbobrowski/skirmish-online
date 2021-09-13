from local import core
from event import Event
from local.unit import Unit
from event_args import EventArgs

import sys
import os

from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task import Task
from panda3d.core import NetDatagram

sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class FetchEvents:
    def __init__(self, manager):
        self.manager = manager
        self.data_handler_mapping = {
            Message.POS_HPR: self.update_pos_hpr,
            Message.NEW_PLAYER: self.update_new_player,
            Message.DISCONNECTION: self.update_disconnection,
            Message.HEALTH: self.update_health,
            Message.TEXT_MSG: self.update_chat,
            Message.ANIMATION: self.update_animation,
            Message.SET_NAME: self.update_name,
            Message.COMBAT_DATA: self.read_combat_data
        }

    def listen_for_updates(self, task):
        if self.manager.reader.data_available():
            datagram = NetDatagram()
            iterator = PyDatagramIterator(datagram)
            if self.manager.reader.get_data(datagram):
                self.process_updates(datagram, iterator)
        return Task.cont

    def process_updates(self, datagram, iterator):
        packet_type = iterator.get_uint8()
        if packet_type not in self.data_handler_mapping:
            return
        self.data_handler_mapping.get(packet_type)(datagram, iterator)

    def update_pos_hpr(self, datagram, iterator):
        while iterator.get_remaining_size() > 0:
            args = EventArgs()
            args.id_ = iterator.get_uint8()
            args.x = iterator.get_float64()
            args.y = iterator.get_float64()
            args.z = iterator.get_float64()
            args.h = iterator.get_float64()
            args.p = iterator.get_float64()
            args.r = iterator.get_float64()
            core.instance.messenger.send(event=Event.PLAYER_CHANGED_POS_HPR, sentArgs=[args])

    def update_new_player(self, datagram, iterator):
        unit = Unit()
        unit.id = iterator.get_uint8()
        unit.name = iterator.get_string()
        unit.health = iterator.get_uint8()
        unit.model = iterator.get_uint8()
        unit.animation = iterator.get_string()
        unit.weapon = iterator.get_uint8()
        unit.x = iterator.get_float64()
        unit.y = iterator.get_float64()
        unit.z = iterator.get_float64()
        unit.h = iterator.get_float64()
        unit.p = iterator.get_float64()
        unit.r = iterator.get_float64()

        args = EventArgs()
        args.unit = unit

        core.instance.messenger.send(event=Event.PLAYER_JOINED, sentArgs=[args])

    def update_disconnection(self, datagram, iterator):
        id_ = iterator.get_uint8()

    def update_health(self, datagram, iterator):
        while iterator.get_remaining_size() > 0:
            id_ = iterator.get_uint8()
            health = iterator.get_uint8()
            core.instance.messenger.send(event=Event.HEALTH_CHANGED, sentArgs=[id_, health])

    def update_chat(self, datagram, iterator):
        name = iterator.get_string()
        time = iterator.get_string()
        message = iterator.get_string()
        core.instance.messenger.send(event=Event.TXT_MSG_FROM_SERVER_RECEIVED, sentArgs=[name, time, message])

    def update_animation(self, datagram, iterator):
        args = EventArgs()
        args.id_ = iterator.get_uint8()
        args.animation = iterator.get_string()
        args.loop = iterator.get_uint8()
        core.instance.messenger.send(event=Event.PLAYER_CHANGED_ANIMATION, sentArgs=[args])

    def update_name(self, datagram, iterator):
        id_ = iterator.get_uint8()
        new_name = iterator.get_string()
        core.instance.messenger.send(event=Event.NAME_CHANGED, sentArgs=[id_, new_name])

    def read_combat_data(self, datagram, iterator):
        args = EventArgs()
        args.action_id = iterator.get_uint8()
        args.hp_change = iterator.get_int8()
        args.hp_change *= 1234  # for cooler effect :-)
        args.source_id = iterator.get_uint8()
        args.target_ids = []
        while iterator.get_remaining_size() > 0:
            args.target_ids.append(iterator.get_uint8())
        core.instance.messenger.send(event=Event.RECEIVED_COMBAT_DATA, sentArgs=[args])

