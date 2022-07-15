from ..domain import Player, PlayerPositionUpdate, PlayerAnimationUpdate, HealthUpdate, NameUpdate, ModelUpdate, WeaponUpdate, Disconnection, ManaUpdate
from server.event.event_user import EventUser
import json
import dataclasses
import logging
from datetime import datetime, timedelta
from protocol.domain import Weapon, Model
import random
from server import config


log = logging.getLogger(__name__)


class PlayerCache(EventUser):
    SET_KEY = "players"
    PREFIX = "player_"
    POSITION_UPDATE_CHANNEL = "position_update"
    MODEL_UPDATE_CHANNEL = "model_update"
    ANIMATION_UPDATE_CHANNEL = "animation_update"
    HEALTH_UPDATE_CHANNEL = "health_update"
    MANA_UPDATE_CHANNEL = "mana_update"
    NAME_UPDATE_CHANNEL = "name_update"
    NEW_PLAYER_CHANNEL = "new_player"
    WEAPON_UPDATE_CHANNEL = "weapon_update"
    DISCONNECT_CHANNEL = "disconnect_channel"

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.last_position_update = datetime.now()
        self.CONNECTION_CHECK_CHANNEL = "connection_check_" + self.session.id

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

        model = random.choice([m.value for m in Model])
        name = {0: "Dark Elf", 1: "Elf", 2: "Kamael", 3: "Dwarf"}[model]
        name = f"{name} [{id_}]"

        player = Player(
            id=id_,
            health=50,
            mana=50,
            model=model,
            name=name,
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

    def delete(self):
        """
        Delete player from redis cache.
        """
        self.session.redis.delete(self.key(self.session.player.id))
        self.session.redis.srem(self.SET_KEY, self.session.player.id)

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
        self.send_event(event=self.NEW_PLAYER_CHANNEL,
                        prepared_data=data)

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

        self.send_event(event=self.POSITION_UPDATE_CHANNEL,
                        prepared_data=data)

        return position_update

    def publish_animation_update(self, animation):
        animation_update = PlayerAnimationUpdate(
            **animation._json(), id=self.session.player.id
        )

        data = json.dumps(dataclasses.asdict(animation_update))

        self.send_event(event=self.ANIMATION_UPDATE_CHANNEL,
                        prepared_data=data)

        return animation_update

    def publish_health_update(self, targets, hp_change) -> None:
        affected_players = []

        for id_ in targets:
            try:
                player = self.load(id_)
                affected_players.append(player)
            except AssertionError:
                continue

        for player in affected_players:
            player.health = min(max((player.health - hp_change, 0)), 100)
            self.save(player)

        health_updates = [HealthUpdate(p.id, p.health) for p in affected_players]

        data = json.dumps([dataclasses.asdict(hu) for hu in health_updates])

        self.send_event(event=self.HEALTH_UPDATE_CHANNEL,
                        prepared_data=data)

    def publish_mana_update(self, targets, mana_change) -> None:
        affected_players = []

        for id_ in targets:
            try:
                player = self.load(id_)
                affected_players.append(player)
            except AssertionError:
                continue

        for player in affected_players:
            player.mana = min(max((player.mana - mana_change, 0)), 100)
            self.save(player)

        mana_updates = [ManaUpdate(p.id, p.mana) for p in affected_players]

        data = json.dumps([dataclasses.asdict(hu) for hu in mana_updates])

        self.send_event(event=self.MANA_UPDATE_CHANNEL,
                        prepared_data=data)

    def publish_name_update(self, name):
        self.session.player = self.load(id_=self.session.player.id)
        self.session.player.name = name
        self.save(self.session.player)
        data = json.dumps(dataclasses.asdict(NameUpdate(self.session.player.id,
                                                        self.session.player.name)))

        self.send_event(event=self.NAME_UPDATE_CHANNEL,
                        prepared_data=data)

    def publish_model_update(self, model):
        self.session.player = self.load(id_=self.session.player.id)
        self.session.player.model_id = model
        self.save(self.session.player)
        data = json.dumps(dataclasses.asdict(ModelUpdate(self.session.player.id,
                                                         self.session.player.model_id)))
        self.send_event(
            event=self.MODEL_UPDATE_CHANNEL,
            prepared_data=data
        )

    def publish_weapon_update(self, weapon_id):
        self.session.player = self.load(id_=self.session.player.id)
        self.session.player.weapon_id = weapon_id
        self.save(self.session.player)
        data = json.dumps(dataclasses.asdict(WeaponUpdate(self.session.player.id,
                                                          self.session.player.weapon_id)))
        self.send_event(
            event=self.WEAPON_UPDATE_CHANNEL,
            prepared_data=data,
        )

    def publish_disconnect(self):
        data = json.dumps(dataclasses.asdict(Disconnection(self.session.player.id)))
        self.send_event(
            event=self.DISCONNECT_CHANNEL,
            prepared_data=data
        )

    def raise_connection_check_event(self):
        self.send_event(
            event=self.CONNECTION_CHECK_CHANNEL,
            prepared_data=json.dumps("")
        )

    # Subscribtions for channels

    def subscribe(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        self.accept_event(
            event=self.POSITION_UPDATE_CHANNEL,
            handler=subscriber
        )

    def subscribe_new_players(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        self.accept_event(
            event=self.NEW_PLAYER_CHANNEL,
            handler=subscriber
        )

    def subscribe_animation_update(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        self.accept_event(
            event=self.ANIMATION_UPDATE_CHANNEL,
            handler=subscriber
        )

    def subscribe_health_update(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        self.accept_event(
            event=self.HEALTH_UPDATE_CHANNEL,
            handler=subscriber
        )

    def subscribe_mana_update(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        self.accept_event(
            event=self.MANA_UPDATE_CHANNEL,
            handler=subscriber
        )

    def subscribe_name_update(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        self.accept_event(
            event=self.NAME_UPDATE_CHANNEL,
            handler=subscriber
        )

    def subscribe_model_update(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        self.accept_event(
            event=self.MODEL_UPDATE_CHANNEL,
            handler=subscriber
        )

    def subscribe_weapon_update(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        self.accept_event(
            event=self.WEAPON_UPDATE_CHANNEL,
            handler=subscriber
        )

    def subscribe_connection_check(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        self.accept_event(
            event=self.CONNECTION_CHECK_CHANNEL,
            handler=subscriber
        )

    def subscribe_disconnect(self, subscriber):
        """
        Creates a thread that will subscribe to the channel
        specific for current user
        """
        self.accept_event(
            event=self.DISCONNECT_CHANNEL,
            handler=subscriber
        )