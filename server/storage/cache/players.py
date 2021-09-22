from ..domain import Player
import json
import dataclasses
import logging


log = logging.getLogger(__name__)


class PlayerCache:
    PREFIX = "player_"

    def __init__(self, session):
        self.session = session

    def key(self, id_=None):
        """
        Prefixed key for session
        """
        if id_ is None:
            id_ = self.session.player.id
        return f"{self.PREFIX}{id_}"

    def load_or_create(self, id_):
        """
        Loads player or creates new
        """
        player_data = self.session.redis.get(self.key(id_))
        log.info(player_data)
        if player_data is None:
            return self.create_from_id(id_)

        return Player(**json.loads(player_data))

    def create_from_id(self, id_):
        """
        Creates new user from id_
        """
        player = Player(
            id_,
            "name",
            50,
            1,
            "stand",
            1,
            -3,
            -5,
            1,
            120,
            0,
            0,
        )
        self.save(player)
        return player

    def save(self, player):
        """
        Saves player
        """
        self.session.redis.set(
            self.key(player.id), json.dumps(dataclasses.asdict(player))
        )
