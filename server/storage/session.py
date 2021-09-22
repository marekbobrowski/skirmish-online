from redis import Redis
import uuid
import logging
import json
from .cache.sessions import SessionCache
from .cache.players import PlayerCache


log = logging.getLogger(__name__)


class SessionManager:
    def __init__(self):
        self.sessions = {}

    def for_connection(self, connection):
        return self.sessions[connection]

    def new_session(self, connection):
        session = Session()
        self.sessions[connection] = session
        return session


class Session:
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.player = None
        self.redis = Redis(host="redis")

        self.cache = SessionCache(self)
        self.cache.store()

        self.player_cache = PlayerCache(self)

    def close(self):
        pass

    def dump(self):
        """
        Dump session data to json
        """
        return json.dumps(
            {
                "player": self.player.id if self.player is not None else None,
            }
        )

    def for_player(self, id_):
        """
        Load player
        """
        self.player = self.player_cache.load_or_create(id_)

    def set_position(self, position):
        """
        Sets player position
        """
        position_update = self.player_cache.publish_position_update(position)
        self.player.update_position(position_update)
        self.player_cache.save(self.player)
