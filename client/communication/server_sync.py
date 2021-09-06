from event import Event

from direct.distributed.PyDatagram import PyDatagram
from direct.showbase.DirectObject import DirectObject

import sys
import os

sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class ServerSync(DirectObject):
    def __init__(self, manager):
        DirectObject.__init__(self)
        self.accept(Event.CLIENT_MAIN_PLAYER_CHANGED_POS_HPR, self.send_pos_hpr)
        self.manager = manager

    def send_pos_hpr(self, character):
        datagram = PyDatagram()
        datagram.add_uint8(Message.POS_HPR)
        datagram.add_float64(character.get_x())
        datagram.add_float64(character.get_y())
        datagram.add_float64(character.get_z())
        datagram.add_float64(character.get_h())
        datagram.add_float64(character.get_p())
        datagram.add_float64(character.get_r())
        self.manager.writer.send(datagram, self.manager.server_connection)

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