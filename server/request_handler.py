from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message
from spell_handler import SpellHandler
import config


class Handler:
    def __init__(self, server):
        self.server = server
        self.action_handler = SpellHandler(server)
        self.data_handler_mapping = {
            Message.ASK_FOR_PASS: self.handle_ask_for_pass,
            Message.ASK_FOR_INITIAL_DATA: self.handle_ask_for_initial_data,
            Message.READY_FOR_UPDATES: self.handle_ready_for_updates,
            Message.POS_HPR: self.handle_pos_hpr,
            Message.DISCONNECTION: self.handle_disconnection,
            Message.ACTION: self.action_handler.handle_action,
            Message.CHAT_MSG: self.handle_chat_message,
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

    def handle_ask_for_pass(self, datagram, iterator):
        name = iterator.get_string()
        class_number = iterator.get_uint8()
        connection = datagram.get_connection()
        allow_player = 0
        # the client had to connect to the server, before he asked for pass
        # so now the server searches for the player object in his connection list
        player = self.server.find_player_by_connection(connection)
        if player is not None:
            player.name = name
            player.class_number = class_number
            player.id = self.server.last_player_id
            self.server.last_player_id += 1
            allow_player = 1
        else:
            allow_player = 0
        response = PyDatagram()
        response.add_uint8(Message.ASK_FOR_PASS)
        response.add_uint8(allow_player)  # 0 - don't allow player to join, 1 - allow player to join
        self.server.writer.send(response, connection)

    def handle_ask_for_initial_data(self, datagram, iterator):
        connection = datagram.get_connection()
        player = self.server.find_player_by_connection(connection)
        if player is None:
            return
        else:
            x, y, z, h, p, r = -3, -5, 1, 120, 0, 0
            player.set_pos_hpr(x, y, z, h, p, r)
            player.health = 50

            response = PyDatagram()
            response.add_uint8(Message.ASK_FOR_INITIAL_DATA)

            # send player his own id, nickname, class and health
            response.add_uint8(player.id)
            response.add_string(player.name)
            response.add_uint8(player.class_number)
            response.add_uint8(player.health)

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
                    response.add_uint8(other_player.class_number)
                    response.add_uint8(other_player.health)
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
        datagram.add_uint8(player.class_number)
        datagram.add_uint8(player.health)
        datagram.add_float64(player.x)
        datagram.add_float64(player.y)
        datagram.add_float64(player.z)
        datagram.add_float64(player.h)
        datagram.add_float64(player.p)
        datagram.add_float64(player.r)

        print('{connection} joined the game with nickname {nickname} and class {player_class}'.format(
            connection=str(connection.get_address()),
            nickname=player.name,
            player_class=player.class_number
        ))
        for other_player in self.server.active_connections:
            if other_player.joined_game and other_player is not player:
                self.server.writer.send(datagram, other_player.connection)

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

    def handle_chat_message(self, datagram, iterator):
        player = self.server.find_player_by_connection(datagram.get_connection())
        if player is None:
            return
        message = iterator.get_string()

        datagram = PyDatagram()
        datagram.add_uint8(Message.CHAT_MSG)
        datagram.add_string(player.name)
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