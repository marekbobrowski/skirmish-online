from direct.distributed.PyDatagram import PyDatagram
from direct.task import Task
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class ServerSync:
    """
    Responsible for sending this client's data to the server.
    The data concerns only the actual skirmish gameplay, such as this client's character position,
    ability usage.
    """
    def __init__(self, manager, world):
        self.manager = manager
        self.world = world

    def send_updates(self, task):
        """
        Continuously (each frame) calls functions that send certain data to the server.
        """
        self.send_pos_hpr()
        return Task.cont

    def send_pos_hpr(self):
        """
        Sends this client's character position and rotation to the server.
        """
        datagram = PyDatagram()
        datagram.add_uint8(Message.POS_HPR)
        datagram.add_float64(self.world.player.character.get_x())
        datagram.add_float64(self.world.player.character.get_y())
        datagram.add_float64(self.world.player.character.get_z())
        datagram.add_float64(self.world.player.character.get_h())
        datagram.add_float64(self.world.player.character.get_p())
        datagram.add_float64(self.world.player.character.get_r())
        self.manager.writer.send(datagram, self.manager.server_connection)

    def send_ability_attempt(self, ability):
        """
        Sends message to the server, stating that this client's user attempted to use a certain ability.
        :param ability: The ability's code.
        :param target: The target's id.
        """
        datagram = PyDatagram()
        datagram.add_uint8(Message.ACTION)
        datagram.add_uint8(ability)
        self.manager.writer.send(datagram, self.manager.server_connection)

    def send_chat_message(self, message):
        """
        Sends a chat message to the server.
        """
        datagram = PyDatagram()
        datagram.add_uint8(Message.TEXT_MSG)
        datagram.add_string(message)
        self.manager.writer.send(datagram, self.manager.server_connection)

    def send_animation(self, animation, loop):
        """
        Send message telling that we using certain animation.
        :param animation: animation name
        :param loop: if it should be looped (0/1)
        """
        datagram = PyDatagram()
        datagram.add_uint8(Message.ANIMATION)
        datagram.add_string(animation)
        datagram.add_uint8(loop)
        self.manager.writer.send(datagram, self.manager.server_connection)