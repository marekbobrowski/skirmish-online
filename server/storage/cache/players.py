from ..domain import Player, PlayerPositionUpdate
import json
import dataclasses
import logging


log = logging.getLogger(__name__)


class PlayerCache:
    PREFIX = "player_"
    POSITION_UPDATE_CHANNEL = "position_update_"

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

    @classmethod
    def channel_for_session(cls, session_id):
        """
        creates unique channel name for session
        """
        return f"{cls.POSITION_UPDATE_CHANNEL}{session_id}"

    def publish_position_update(self, position):
        """
        Pushes position update
        """
        position_update = PlayerPositionUpdate(
            **position._json(), player_id=self.session.player.id
        )

        for session_id in self.session.cache.get_other_sessions():
            self.session.redis.publish(
                self.channel_for_session(session_id),
                json.dumps(dataclasses.asdict(position_update)),
            )

        return position_update

    def subscribe(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        p = self.session.redis.pubsub()
        p.subscribe(**{self.channel_for_session(self.session.id): subscriber})
        thread = p.run_in_thread(sleep_time=0.001)
        return thread
