from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram
import sys
import os
sys.path.append(os.path.abspath(os.path.join('..')))
from protocol.message import Message
from action_handler import ActionHandler


# noinspection PyArgumentList
class Handler:
    def __init__(self, server):
        self.server = server
        self.action_handler = ActionHandler(server)

    def handle_data(self, datagram):
        iterator = PyDatagramIterator(datagram)
        packet_type = iterator.get_uint8()
        if packet_type == Message.ASK_FOR_PASS:
            self.handle_ask_for_pass(datagram, iterator)
        elif packet_type == Message.ASK_FOR_INITIAL_DATA:
            self.handle_ask_for_initial_data(datagram, iterator)
        elif packet_type == Message.READY_FOR_UPDATES:
            self.handle_ready_for_updates(datagram, iterator)
        elif packet_type == Message.POS_HPR:
            self.handle_pos_hpr(datagram, iterator)
        elif packet_type == Message.DISCONNECTION:
            self.handle_disconnection(datagram, iterator)
        elif packet_type == Message.ACTION:
            self.action_handler.handle_action(datagram, iterator)
        elif packet_type == Message.CHAT_MSG:
            self.handle_chat_message(datagram, iterator)

    def handle_ask_for_pass(self, datagram, iterator):
        name = iterator.get_string()
        class_number = iterator.get_uint8()
        connection = datagram.get_connection()
        allow_player = 0
        # the client had to connect to the server, before he asked for pass
        # so now the server searches for the player object in his connection list
        player = self.server.find_player_by_connection(connection)
        if player is not None:
            player.set_name(name)
            player.set_class_number(class_number)
            player.set_id(self.server.last_player_id)
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
            response.add_uint8(player.get_id())
            response.add_string(player.get_name())
            response.add_uint8(player.get_class_number())
            response.add_uint8(player.health)

            # send player his own position and rotation
            response.add_float64(player.get_x())
            response.add_float64(player.get_y())
            response.add_float64(player.get_z())
            response.add_float64(player.get_h())
            response.add_float64(player.get_p())
            response.add_float64(player.get_r())

            active_players = self.server.get_number_of_active_players()

            # send players' id's, names and positions & rotations
            for i, other_player in enumerate(self.server.active_connections):
                if other_player is not player and other_player.get_joined_game() and i < active_players:
                    # order: id, name, class, x, y, z, h, p, r
                    response.add_uint8(other_player.get_id())
                    response.add_string(other_player.get_name())
                    response.add_uint8(other_player.get_class_number())
                    response.add_uint8(other_player.health)
                    response.add_float64(other_player.get_x())
                    response.add_float64(other_player.get_y())
                    response.add_float64(other_player.get_z())
                    response.add_float64(other_player.get_h())
                    response.add_float64(other_player.get_p())
                    response.add_float64(other_player.get_r())
            self.server.writer.send(response, connection)

    def handle_ready_for_updates(self, datagram, iterator):
        connection = datagram.get_connection()
        player = self.server.find_player_by_connection(connection)

        if player is None:
            return
        else:
            player.set_joined_game(True)

        # send info about new player to everyone else
        datagram = PyDatagram()
        datagram.add_uint8(Message.NEW_PLAYER)
        datagram.add_uint8(player.get_id())
        datagram.add_string(player.get_name())
        datagram.add_uint8(player.get_class_number())
        datagram.add_uint8(player.health)
        datagram.add_float64(player.get_x())
        datagram.add_float64(player.get_y())
        datagram.add_float64(player.get_z())
        datagram.add_float64(player.get_h())
        datagram.add_float64(player.get_p())
        datagram.add_float64(player.get_r())

        print('{connection} joined the game with nickname {nickname} and class {player_class}'.format(
            connection=str(connection.get_address()),
            nickname=player.get_name(),
            player_class=player.get_class_number()
        ))
        for other_player in self.server.active_connections:
            if other_player.get_joined_game() and other_player is not player:
                self.server.writer.send(datagram, other_player.get_connection())

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
            id_ = player.get_id()
            del player
            for other_player in self.server.active_connections:
                if other_player.get_joined_game():
                    datagram = PyDatagram()
                    datagram.add_uint8(Message.DISCONNECTION)
                    datagram.add_uint8(id_)
                    self.server.writer.send(datagram, other_player.get_connection())

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
                self.server.writer.send(datagram, player.get_connection())


