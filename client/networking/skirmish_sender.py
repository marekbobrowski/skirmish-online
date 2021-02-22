from direct.distributed.PyDatagram import PyDatagram
from direct.task import Task
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message


class SkirmishSender:
    def __init__(self, skirmish, writer, server_connection, manager):
        self.manager = manager
        self.skirmish = skirmish
        self.writer = writer
        self.server_connection = server_connection

    def send_updates(self, task):
        if self.manager.connected:
            self.send_pos_hpr()
            return Task.cont
        else:
            return Task.done

    def send_pos_hpr(self):
        datagram = PyDatagram()
        datagram.add_uint8(Message.POS_HPR)
        datagram.add_float64(self.skirmish.player.get_x())
        datagram.add_float64(self.skirmish.player.get_y())
        datagram.add_float64(self.skirmish.player.get_z())
        datagram.add_float64(self.skirmish.player.get_h())
        datagram.add_float64(self.skirmish.player.get_p())
        datagram.add_float64(self.skirmish.player.get_r())
        self.writer.send(datagram, self.server_connection)

    def send_action_attempt(self, action, target):
        datagram = PyDatagram()
        datagram.add_uint8(Message.ACTION)
        datagram.add_uint8(action)
        datagram.add_uint8(target)
        self.writer.send(datagram, self.server_connection)

