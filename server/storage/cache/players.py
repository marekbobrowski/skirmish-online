from ..domain import Player, PlayerPositionUpdate, PlayerAnimationUpdate, HealthUpdate, NameUpdate
import json
import dataclasses
import logging
from datetime import datetime, timedelta
from protocol.domain import Weapon, Model
import random
from server import config


log = logging.getLogger(__name__)


class PlayerCache:
    SET_KEY = "players"
    PREFIX = "player_"
    POSITION_UPDATE_CHANNEL = "position_update"
    ANIMATION_UPDATE_CHANNEL = "animation_update"
    HEALTH_UPDATE_CHANNEL = "health_update"
    NAME_UPDATE_CHANNEL = "name_update"
    NEW_PLAYER_CHANNEL = "new_player"

    def __init__(self, session):
        self.session = session
        self.last_position_update = datetime.now()

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
            model=random.choice([m.value for m in Model]),
            animation="stand",
            loop=1,
            weapon=random.choice([w.value for w in Weapon]),
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

    # channel publication

    def publish_new_player(self, player):
        """
        Publishes new player
        """
        self.save(player)
        self.session.redis.sadd(self.SET_KEY, player.id)
        self.session.player_position_cache.update_position(player)

        data = json.dumps(dataclasses.asdict(player))

        self.session.redis.publish(
            self.NEW_PLAYER_CHANNEL,
            data,
        )

    def publish_position_update(self, position):
        """
        Pushes position update, only if some time passed
        """
        event_dtime = datetime.now()

        if event_dtime - self.last_position_update < timedelta(
            milliseconds=config.position_update_delay
        ):
            return

        self.last_position_update = event_dtime
        position_update = PlayerPositionUpdate(
            **position._json(), id=self.session.player.id
        )

        self.session.player_position_cache.update_position(position_update)

        data = dataclasses.asdict(position_update)
        data["event_dtime"] = event_dtime.timestamp()
        data = json.dumps(data)

        self.session.redis.publish(
            self.POSITION_UPDATE_CHANNEL,
            data,
        )

        return position_update

    def publish_animation_update(self, animation):
        """
        Self explanatory name!!!
        """
        animation_update = PlayerAnimationUpdate(
            **animation._json(), id=self.session.player.id
        )

        data = json.dumps(dataclasses.asdict(animation_update))

        self.session.redis.publish(
            self.ANIMATION_UPDATE_CHANNEL,
            data,
        )

        return animation_update

    def publish_health_update(self, targets, hp_change) -> None:
        """
        Self explanatory name!!!
        """
        affected_players = [self.load(id_) for id_ in targets]

        for player in affected_players:
            player.health = max((player.health - hp_change, 0))
            self.save(player)

        health_updates = [HealthUpdate(p.id, p.health) for p in affected_players]
        data = json.dumps([dataclasses.asdict(hu) for hu in health_updates])

        self.session.redis.publish(
            self.HEALTH_UPDATE_CHANNEL,
            data,
        )

    def publish_name_update(self, name):
        self.session.player.name = name
        self.save(self.session.player)
        data = json.dumps(dataclasses.asdict(NameUpdate(self.session.player.id,
                                                        self.session.player.name)))
        self.session.redis.publish(
            self.NAME_UPDATE_CHANNEL,
            data,
        )


    # Subscribtions for channels

    def subscribe(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        p = self.session.redis.pubsub()
        p.subscribe(**{self.POSITION_UPDATE_CHANNEL: subscriber})
        thread = p.run_in_thread(sleep_time=0.001)
        return thread

    def subscribe_new_players(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        p = self.session.redis.pubsub()
        p.subscribe(**{self.NEW_PLAYER_CHANNEL: subscriber})
        thread = p.run_in_thread(sleep_time=0.001)
        return thread

    def subscribe_animation_update(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        p = self.session.redis.pubsub()
        p.subscribe(**{self.ANIMATION_UPDATE_CHANNEL: subscriber})
        thread = p.run_in_thread(sleep_time=0.001)
        return thread

    def subscribe_health_update(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        p = self.session.redis.pubsub()
        p.subscribe(**{self.HEALTH_UPDATE_CHANNEL: subscriber})
        thread = p.run_in_thread(sleep_time=0.001)
        return thread

    def subscribe_name_update(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        p = self.session.redis.pubsub()
        p.subscribe(**{self.NAME_UPDATE_CHANNEL: subscriber})
        thread = p.run_in_thread(sleep_time=0.001)
        return thread
