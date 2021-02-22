from direct.distributed.PyDatagram import PyDatagram
from direct.task import Task
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class SkirmishSender:
    """
    Responsible for sending this client's data to the server.
    The data concerns only the actual skirmish gameplay, such as this client's character position,
    ability usage.
    """
    def __init__(self, manager, skirmish):
        self.manager = manager
        self.skirmish = skirmish

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
        datagram.add_float64(self.skirmish.player.get_x())
        datagram.add_float64(self.skirmish.player.get_y())
        datagram.add_float64(self.skirmish.player.get_z())
        datagram.add_float64(self.skirmish.player.get_h())
        datagram.add_float64(self.skirmish.player.get_p())
        datagram.add_float64(self.skirmish.player.get_r())
        self.manager.writer.send(datagram, self.manager.server_connection)

    def send_ability_attempt(self, ability, target):
        """
        Sends message to the server, stating that this client's user attempted to use a certain ability.
        :param ability: The ability's code.
        :param target: The target's id.
        """
        datagram = PyDatagram()
        datagram.add_uint8(Message.ACTION)
        datagram.add_uint8(ability)
        datagram.add_uint8(target)
        self.manager.writer.send(datagram, self.manager.server_connection)

