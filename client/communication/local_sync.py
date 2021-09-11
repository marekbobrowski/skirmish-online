from local import core
from event import Event
from local.player import Player

import sys
import os

from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.task import Task
from panda3d.core import NetDatagram

sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class LocalSync:
    def __init__(self, manager):
        self.manager = manager
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
            id_ = iterator.get_uint8()
            x = iterator.get_float64()
            y = iterator.get_float64()
            z = iterator.get_float64()
            h = iterator.get_float64()
            p = iterator.get_float64()
            r = iterator.get_float64()
            core.instance.messenger.send(event=Event.PLAYER_CHANGED_POS_HPR, sentArgs=[id_, x, y, z, h, p, r])

    def update_new_player(self, datagram, iterator):
        player = Player()
        player.id = iterator.get_uint8()
        player.name = iterator.get_string()
        player.health = iterator.get_uint8()
        player.model = iterator.get_uint8()
        player.animation = iterator.get_string()
        player.x = iterator.get_float64()
        player.y = iterator.get_float64()
        player.z = iterator.get_float64()
        player.h = iterator.get_float64()
        player.p = iterator.get_float64()
        player.r = iterator.get_float64()
        core.instance.messenger.send(event=Event.PLAYER_JOINED, sentArgs=[player])

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
        id_ = iterator.get_uint8()
        animation = iterator.get_string()
        loop = iterator.get_uint8()
        core.instance.messenger.send(event=Event.PLAYER_CHANGED_ANIMATION, sentArgs=[None, id_, animation, loop])

    def update_action(self, datagram, iterator):
        return
        id_ = iterator.get_uint8()
        action_id = iterator.get_uint8()
        cd_time = iterator.get_uint8()
        print('Player with id ' + str(id_) + ' used action: ' + str(action_id) + 'and dealt x dmg.')
        if id_ == self.world.player.id:
            self.world.abilities.trigger_cooldown(action_id, cd_time)

    def update_name(self, datagram, iterator):
        id_ = iterator.get_uint8()
        new_name = iterator.get_string()
        core.instance.messenger.send(event=Event.NAME_CHANGED, sentArgs=[id_, new_name])
