from event import Event
from local import core

from direct.distributed.PyDatagram import PyDatagram
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task

import sys
import os

sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class SendRequests(DirectObject):
    def __init__(self, manager):
        DirectObject.__init__(self)
        self.manager = manager
        self.accept(Event.CLIENT_STARTED_ANIMATION, self.send_animation)
        self.accept(Event.TXT_MSG_TO_SERVER_TYPED, self.send_chat_message)

    def send_pos_hpr(self, unit):
        datagram = PyDatagram()
        datagram.add_uint8(Message.POS_HPR)
        datagram.add_float64(unit.actor.get_x())
        datagram.add_float64(unit.actor.get_y())
        datagram.add_float64(unit.actor.get_z())
        datagram.add_float64(unit.actor.get_h())
        datagram.add_float64(unit.actor.get_p())
        datagram.add_float64(unit.actor.get_r())
        self.manager.writer.send(datagram, self.manager.server_connection)
        return Task.cont

    def send_ability_attempt(self, ability):
        datagram = PyDatagram()
        datagram.add_uint8(Message.ACTION)
        datagram.add_uint8(ability)
        self.manager.writer.send(datagram, self.manager.server_connection)

    def send_chat_message(self, message):
        datagram = PyDatagram()
        datagram.add_uint8(Message.TEXT_MSG)
        datagram.add_string(message)
        self.manager.writer.send(datagram, self.manager.server_connection)

    def send_animation(self, animation, loop):
        datagram = PyDatagram()
        datagram.add_uint8(Message.ANIMATION)
        datagram.add_string(animation)
        datagram.add_uint8(loop)
        self.manager.writer.send(datagram, self.manager.server_connection)
