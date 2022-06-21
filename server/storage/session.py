from redis import Redis
import uuid
import logging
import json
from server.connection_dependant.connection_dependant_mgr import ConnectionDependantManager
from server.connection_dependant.connection_dependant import ConnectionDependantObj
from server.event.event_user import EventUser
from .cache.sessions import SessionCache
from .cache.players import PlayerCache
from .cache.player_position import PlayerPositionCache
from .cache.spells import SpellCache
from .cache.text_message import TextMessageCache


log = logging.getLogger(__name__)


class SessionManager(ConnectionDependantManager):
    def __init__(self):
        """
        SessionManager is a container for all active sessions
        """
        self.sessions = {}
        super().__init__(self.sessions)

    def for_connection(self, connection):
        """
        Fetches session assigned for connection
        """
        return self.sessions[connection]

    def new_session(self, connection):
        """
        Creastes new session
        """
        session = Session()
        self.sessions[connection] = session
        return session

    def stop_listening_threads(self):
        for session in self.sessions.values():
            session.stop_listening_threads()


class Session(ConnectionDependantObj):
    def __init__(self):
        """
        Creates empty session
        """
        self.id = uuid.uuid4().hex
        self.player = None
        self.redis = Redis(host="redis")

        self.cache = SessionCache(self)
        self.cache.store()

        self.player_cache = PlayerCache(self)
        self.player_position_cache = PlayerPositionCache(self)
        self.spell_cache = SpellCache(self)
        self.text_message_cache = TextMessageCache(self)
        self.ready_for_continuous_sync = False

    def stop_listening_threads(self):
        for member in self.__dict__.values():
            if isinstance(member, EventUser):
                member.stop_listening_threads()

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
        if position_update is not None:
            self.player = self.player_cache.load(self.player.id)
            self.player.update_position(position_update)
            self.player_cache.save(self.player)

    def set_animation(self, animation):
        """
        Sets player animation
        """
        animation_update = self.player_cache.publish_animation_update(
            animation,
        )
        self.player = self.player_cache.load(self.player.id)
        self.player.update_animation(animation_update)
        self.player_cache.save(self.player)

