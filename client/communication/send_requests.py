from ..event import Event
from ..local import core

from direct.distributed.PyDatagram import PyDatagram
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task

from protocol.message import Message

from utils.unspammer import RequestUnspammer


class SendRequests(DirectObject):
    def __init__(self, manager):
        DirectObject.__init__(self)
        self.manager = manager
        self.accept(Event.CLIENT_STARTED_ANIMATION, self.send_animation)
        self.accept(Event.TXT_MSG_TO_SERVER_TYPED, self.send_chat_message)
        self.accept(Event.CLIENT_SPELL_ATTEMPT, self.send_ability_attempt)

        self.guardian = RequestUnspammer()

    def write(self, datagram, safe=False):
        if self.guardian.clean() or safe:
            self.manager.writer.send(datagram, self.manager.server_connection)

    def send_pos_hpr(self, node, ref_node):
        datagram = PyDatagram()
        datagram.add_uint8(Message.POS_HPR)
        datagram.add_float64(node.get_x(ref_node))
        datagram.add_float64(node.get_y(ref_node))
        datagram.add_float64(node.get_z(ref_node))
        datagram.add_float64(node.get_h(ref_node))
        datagram.add_float64(node.get_p(ref_node))
        datagram.add_float64(node.get_r(ref_node))
        self.write(datagram)
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
