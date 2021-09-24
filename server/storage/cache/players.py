from ..domain import Player, PlayerPositionUpdate, PlayerAnimationUpdate
import json
import dataclasses
import logging


log = logging.getLogger(__name__)


class PlayerCache:
    SET_KEY = "players"
    PREFIX = "player_"
    POSITION_UPDATE_CHANNEL = "position_update_"
    ANIMATION_UPDATE_CHANNEL = "animation_update_"
    NEW_PLAYER_CHANNEL = "new_player_"

    def __init__(self, session):
        self.session = session

    def key(self, id_=None):
        """
        Prefixed key for session
        """
        if id_ is None:
            id_ = self.session.player.id
        if isinstance(id_, bytes):
            return f"{self.PREFIX}{id_.decode()}"
        return f"{self.PREFIX}{id_}"

    def load(self, id_):
        """
        Loads player
        """
        player_data = self.session.redis.get(self.key(id_))
        assert player_data is not None, self.key(id_)
        return Player(**json.loads(player_data))

    def load_or_create(self, id_):
        """
        Loads player or creates new
        """
        try:
            return self.load(id_)
        except AssertionError:
            return self.create_from_id(id_)

    def create_from_id(self, id_):
        """
        Creates new user from id_
        """
        player = Player(
            id=id_,
            name=f"name{id_}",
            health=50,
            model=1,
            animation="stand",
            loop=1,
            weapon=1,
            x=-3,
            y=-5,
            z=1,
            h=120,
            p=0,
            r=0,
        )
        self.publish_new_player(player)
        return player

    def save(self, player):
        """
        Saves player
        """
        self.session.redis.set(
            self.key(player.id), json.dumps(dataclasses.asdict(player))
        )

    def all_player_ids(self):
        """
        Returns all player ids
        """
        members = self.session.redis.smembers(self.SET_KEY)
        return members

    def all_players(self):
        """
        Returns all players objects
        """
        return [self.load(id_) for id_ in self.all_player_ids()]

    def other_player_ids(self):
        """
        Returns other player ids
        """
        members = self.all_player_ids()
        other_ids = {int(m.decode()) for m in members} - {self.session.player.id}
        return other_ids

    def other_players(self):
        """
        Returns other players
        """
        return [self.load(id_) for id_ in self.other_player_ids()]

    # channels for publication

    @classmethod
    def channel_for_session(cls, session_id):
        """
        creates unique channel name for session
        """
        return f"{cls.POSITION_UPDATE_CHANNEL}{session_id}"

    @classmethod
    def new_player_channel_for_session(cls, session_id):
        """
        creates unique channel name for session
        """
        return f"{cls.NEW_PLAYER_CHANNEL}{session_id}"

    @classmethod
    def animation_update_channel_for_session(cls, session_id):
        """
        creates unique channel name for session
        """
        return f"{cls.ANIMATION_UPDATE_CHANNEL}{session_id}"

    # channel publication

    def publish_new_player(self, player):
        """
        Publishes new player
        """
        self.save(player)
        self.session.redis.sadd(self.SET_KEY, player.id)
        self.session.player_position_cache.update_position(player)

        for session_id in self.session.cache.get_other_sessions():
            self.session.redis.publish(
                self.new_player_channel_for_session(session_id),
                json.dumps(dataclasses.asdict(player)),
            )

    def publish_position_update(self, position):
        """
        Pushes position update
        """
        position_update = PlayerPositionUpdate(
            **position._json(), id=self.session.player.id
        )

        self.session.player_position_cache.update_position(position_update)

        for session_id in self.session.cache.get_other_sessions():
            self.session.redis.publish(
                self.channel_for_session(session_id),
                json.dumps(dataclasses.asdict(position_update)),
            )

        return position_update

    def publish_animation_update(self, animation, including_self=False):
        """
        Self explanatory name!!!
        """
        animation_update = PlayerAnimationUpdate(
            **animation._json(), id=self.session.player.id
        )

        sessions = self.session.cache.get_other_sessions()
        if including_self is True:
            sessions.add(self.session.id)

        for session_id in sessions:
            self.session.redis.publish(
                self.animation_update_channel_for_session(session_id),
                json.dumps(dataclasses.asdict(animation_update)),
            )

        return animation_update

    # Subscribtions for channels

    def subscribe(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        p = self.session.redis.pubsub()
        p.subscribe(**{self.channel_for_session(self.session.id): subscriber})
        thread = p.run_in_thread(sleep_time=0.001)
        return thread

    def subscribe_new_players(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        p = self.session.redis.pubsub()
        p.subscribe(
            **{self.new_player_channel_for_session(self.session.id): subscriber}
        )
        thread = p.run_in_thread(sleep_time=0.001)
        return thread

    def subscribe_animation_update(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        p = self.session.redis.pubsub()
        p.subscribe(
            **{self.animation_update_channel_for_session(self.session.id): subscriber}
        )
        thread = p.run_in_thread(sleep_time=0.001)
        return thread
