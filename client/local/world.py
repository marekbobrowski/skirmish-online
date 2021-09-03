from local.player import Player
from local import asset_names
from local import core

class World:
    """
    Holds the world state - information about players.
    """
    def __init__(self):
        self.player = None
        self.other_players = []

    def load_world_state(self, iterator, datagram):
        id_ = iterator.get_uint8()
        name = iterator.get_string()
        class_number = iterator.get_uint8()
        health = iterator.get_uint8()
        x = iterator.get_float64()
        y = iterator.get_float64()
        z = iterator.get_float64()
        h = iterator.get_float64()
        p = iterator.get_float64()
        r = iterator.get_float64()
        self.create_main_player(id_, class_number, name, health, x, y, z, h, p, r)
        self.player.health = health
        while iterator.get_remaining_size() > 0:
            id_ = iterator.get_uint8()
            name = iterator.get_string()
            class_number = iterator.get_uint8()
            health = iterator.get_uint8()
            x = iterator.get_float64()
            y = iterator.get_float64()
            z = iterator.get_float64()
            h = iterator.get_float64()
            p = iterator.get_float64()
            r = iterator.get_float64()
            self.create_other_player(id_, class_number, name, health, x, y, z, h, p, r)
        core.instance.messenger.send('player-base-updated')

    def create_main_player(self, id_, class_number, name, health, x, y, z, h, p, r):
        player = Player(asset_names.night_elf, id_)
        player.class_number = class_number
        player.name = name
        player.health = health
        player.character.set_pos_hpr(x, y, z, h, p, r)
        self.player = player

    def create_other_player(self, id_, class_number, name, health, x, y, z, h, p, r):
        player = Player(asset_names.night_elf, id_)
        player.class_number = class_number
        player.name = name
        player.health = health
        player.character.set_pos_hpr(x, y, z, h, p, r)
        self.other_players.append(player)

    def get_player_by_id(self, id_):
        for other_player in self.other_players:
            if other_player.id == id_:
                return other_player
        return None

    def update_player_pos_hpr(self, id_, x, y, z, h, p, r):
        player = self.get_player_by_id(id_)
        if player is not None:
            player.character.set_pos_hpr(x, y, z, h, p, r)
