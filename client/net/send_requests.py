from ..event import Event
from ..local import core

from direct.distributed.PyDatagram import PyDatagram
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task

from protocol.message import Message

import time


class SendRequests(DirectObject):
    def __init__(self, manager):
        DirectObject.__init__(self)
        self.manager = manager
        self.accept(Event.CLIENT_STARTED_ANIMATION, self.send_animation)
        self.accept(Event.TXT_MSG_TO_SERVER_TYPED, self.send_chat_message)
        self.accept(Event.CLIENT_SPELL_ATTEMPT, self.send_ability_attempt)

        self.last_position = tuple()

    def write(self, datagram, safe=False):
        self.manager.writer.send(datagram, self.manager.server_connection)

    def send_pos_hpr(self, node, ref_node):
        position = (
            node.get_x(ref_node),
            node.get_y(ref_node),
            node.get_z(ref_node),
            node.get_h(ref_node),
            node.get_p(ref_node),
            node.get_r(ref_node),
        )

        if position != self.last_position:
            datagram = PyDatagram()
            datagram.add_uint8(Message.POS_HPR)
            datagram.add_float64(position[0])
            datagram.add_float64(position[1])
            datagram.add_float64(position[2])
            datagram.add_float64(position[3])
            datagram.add_float64(position[4])
            datagram.add_float64(position[5])
            self.write(datagram)
            self.last_position = position
            time.sleep(0.001)
        return Task.cont

    def send_ability_attempt(self, ability):
        datagram = PyDatagram()
        datagram.add_uint8(Message.ACTION)
        datagram.add_uint8(ability)
        self.write(datagram, True)

    def send_chat_message(self, message):
        datagram = PyDatagram()
        datagram.add_uint8(Message.TEXT_MSG)
        datagram.add_string(message)
        self.write(datagram, True)

    def send_animation(self, animation, loop):
        datagram = PyDatagram()
        datagram.add_uint8(Message.ANIMATION)
        datagram.add_string(animation)
        datagram.add_uint8(loop)
        self.write(datagram, True)
