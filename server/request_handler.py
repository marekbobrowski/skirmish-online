from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram
import sys
import os
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message
from spell_handler import SpellHandler
import config


class Handler:
    def __init__(self, server):
        self.server = server
        self.action_handler = SpellHandler(server)
        self.data_handler_mapping = {
            Message.WORLD_STATE: self.handle_request_world_state,
            Message.READY_FOR_SYNC: self.handle_ready_for_updates,
            Message.POS_HPR: self.handle_pos_hpr,
            Message.DISCONNECTION: self.handle_disconnection,
            Message.ACTION: self.action_handler.handle_action,
            Message.TEXT_MSG: self.handle_text_msg,
            Message.ANIMATION: self.handle_animation,
            Message.WELCOME_MSG: self.handle_welcome_msg_request
        }

    def handle_data(self, datagram):
        iterator = PyDatagramIterator(datagram)
        packet_type = iterator.get_uint8()
        if packet_type not in self.data_handler_mapping:
            return
        self.data_handler_mapping[packet_type](datagram, iterator)

    def handle_welcome_msg_request(self, datagram, iterator):
        response = PyDatagram()
        response.add_uint8(Message.WELCOME_MSG)
        response.add_uint8(len(config.welcome_msg))
        for line in config.welcome_msg:
            response.add_string(line)
        self.server.writer.send(response, datagram.get_connection())

    def handle_request_world_state(self, datagram, iterator):
        connection = datagram.get_connection()
        player = self.server.find_player_by_connection(connection)
        if player is None:
            return
        else:
            x, y, z, h, p, r = -3, -5, 1, 120, 0, 0
            player.name = 'nameless_idiot'
            player.set_pos_hpr(x, y, z, h, p, r)
            player.health = 50
            player.model = 0
            player.animation = 'stand'
            player.id = self.server.last_player_id
            self.server.last_player_id += 1

            response = PyDatagram()
            response.add_uint8(Message.WORLD_STATE)

            # send player his own id, nickname, class and health
            response.add_uint8(player.id)
            response.add_string(player.name)
            response.add_uint8(player.health)
            response.add_uint8(player.model)
            response.add_string(player.animation)

            # send player his own position and rotation
            response.add_float64(player.x)
            response.add_float64(player.y)
            response.add_float64(player.z)
            response.add_float64(player.h)
            response.add_float64(player.p)
            response.add_float64(player.r)

            active_players = self.server.get_number_of_active_players()

            # send players' id's, names and positions & rotations
            for i, other_player in enumerate(self.server.active_connections):
                if other_player is not player and other_player.joined_game and i < active_players:
                    response.add_uint8(other_player.id)
                    response.add_string(other_player.name)
                    response.add_uint8(other_player.health)
                    response.add_uint8(other_player.model)
                    response.add_string(other_player.animation)
                    response.add_float64(other_player.x)
                    response.add_float64(other_player.y)
                    response.add_float64(other_player.z)
                    response.add_float64(other_player.h)
                    response.add_float64(other_player.p)
                    response.add_float64(other_player.r)
            self.server.writer.send(response, connection)

    def handle_ready_for_updates(self, datagram, iterator):
        connection = datagram.get_connection()
        player = self.server.find_player_by_connection(connection)

        if player is None:
            return
        else:
            player.joined_game = True

        # send info about new player to everyone else
        datagram = PyDatagram()
        datagram.add_uint8(Message.NEW_PLAYER)
        datagram.add_uint8(player.id)
        datagram.add_string(player.name)
        datagram.add_uint8(player.health)
        datagram.add_uint8(player.model)
        datagram.add_string(player.animation)
        datagram.add_float64(player.x)
        datagram.add_float64(player.y)
        datagram.add_float64(player.z)
        datagram.add_float64(player.h)
        datagram.add_float64(player.p)
        datagram.add_float64(player.r)

        for other_player in self.server.active_connections:
            if other_player.joined_game and other_player is not player:
                self.server.writer.send(datagram, other_player.connection)

        welcome_msg_datagram = PyDatagram()
        welcome_msg_datagram.add_uint8(Message.TEXT_MSG)
        welcome_msg_datagram.add_string('')
        welcome_msg_datagram.add_string('')
        welcome_msg_datagram.add_string(config.welcome_msg)
        self.server.writer.send(welcome_msg_datagram, connection)

    def handle_pos_hpr(self, datagram, iterator):
        player = self.server.find_player_by_connection(datagram.get_connection())
        if player is not None:
            x = iterator.get_float64()
            y = iterator.get_float64()
            z = iterator.get_float64()
            h = iterator.get_float64()
            p = iterator.get_float64()
            r = iterator.get_float64()
            player.set_pos_hpr(x, y, z, h, p, r)

    def handle_disconnection(self, datagram, iterator):
        connection = datagram.get_connection()
        player = self.server.find_player_by_connection(connection)
        if player is not None:
            self.server.active_connections.remove(player)
            print(str(connection.get_address()) + ' disconnected.')
            self.server.manager.close_connection(connection)
            id_ = player.id
            del player
            for other_player in self.server.active_connections:
                if other_player.joined_game:
                    datagram = PyDatagram()
                    datagram.add_uint8(Message.DISCONNECTION)
                    datagram.add_uint8(id_)
                    self.server.writer.send(datagram, other_player.connection)

    def handle_text_msg(self, datagram, iterator):
        player = self.server.find_player_by_connection(datagram.get_connection())
        if player is None:
            return
        message = iterator.get_string()
        words = message.split()

        if words[0] == '/setname':
            new_name = words[1]
            player.name = new_name
            datagram = PyDatagram()

            datagram.add_uint8(Message.SET_NAME)
            datagram.add_uint8(player.id)
            datagram.add_string(player.name)
            for player in self.server.active_connections:
                if player.joined_game:
                    self.server.writer.send(datagram, player.connection)
            return

        datagram = PyDatagram()
        datagram.add_uint8(Message.TEXT_MSG)
        datagram.add_string(player.name)
        datagram.add_string(datetime.now().strftime("%H:%M:%S"))
        datagram.add_string(message)

        for player in self.server.active_connections:
            if player.joined_game:
                self.server.writer.send(datagram, player.connection)

    def handle_animation(self, datagram, iterator):
        animation = iterator.get_string()
        loop = iterator.get_uint8()
        the_player = self.server.find_player_by_connection(datagram.get_connection())

        datagram = PyDatagram()
        datagram.add_uint8(Message.ANIMATION)
        datagram.add_uint8(the_player.id)
        datagram.add_string(animation)
        datagram.add_uint8(loop)
        for player in self.server.active_connections:
            if player.joined_game and player is not the_player:
                self.server.writer.send(datagram, player.connection)
