from local.player import Player
from local import asset_names
from local import core

from event import Event
from direct.showbase.DirectObject import DirectObject


class World(DirectObject):
    """
    Holds the world state - information about players.
    """
    def __init__(self):
        DirectObject.__init__(self)
        self.player = None
        self.other_players = []
        self.accept(Event.PLAYER_JOINED, self.add_other_player)

    def get_other_player_by_id(self, id_):
        for other_player in self.other_players:
            if other_player.id == id_:
                return other_player
        return None

    def get_any_player_by_id(self, id_):
        if id_ == self.player.id:
            return self.player
        return self.get_other_player_by_id(id_)

    def set_main_player(self, player):
        self.player = player

    def add_other_player(self, player):
        self.other_players.append(player)

