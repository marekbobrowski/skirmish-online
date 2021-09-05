from local.player import Player
from local import asset_names
from local import core

from event import Event


class World:
    """
    Holds the world state - information about players.
    """
    def __init__(self):
        self.player = None
        self.other_players = []

    def get_other_player_by_id(self, id_):
        for other_player in self.other_players:
            if other_player.id == id_:
                return other_player
        return None

    def get_any_player_by_id(self, id_):
        if id_ == self.player.id:
            return self.player
        return self.get_other_player_by_id(id_)
