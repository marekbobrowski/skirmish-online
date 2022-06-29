from ..domain import SpellUpdate
from server.event.event_user import EventUser
import json
import dataclasses
from datetime import datetime, timedelta
import logging

log = logging.getLogger(__name__)


class SpellCache(EventUser):
    HMSET_PREFIX = "player_trigger_times_"
    SPELL_UPDATE_CHANNEL = "spell_update_"
    COOLDOWN_TIME_PER_SPELL_ID = {
        0: 1.0,
        1: 1.0,
        2: 1.0,
        3: 1.0
    }

    def __init__(self, session):
        super().__init__()
        self.session = session

    def key(self):
        """
        Prefixed key for dict of trigger times.
        """
        return f"{self.HMSET_PREFIX}{self.session.player.id}"

    @classmethod
    def spell_update_channel_for_session(cls, session_id):
        """
        Creates a unique channel name for the session.
        """
        return f"{cls.SPELL_UPDATE_CHANNEL}{session_id}"

    def publish_spell_update(self, spell):
        """
        Broadcasts a spell.
        """
        spell_update = SpellUpdate(**spell._json(), id=self.session.player.id)
        data = json.dumps(dataclasses.asdict(spell_update))

        for session_id in self.session.cache.get_other_sessions():
            self.session.redis.publish(
                self.spell_update_channel_for_session(session_id),
                data,
            )

        return spell_update

    def subscribe(self, subscriber):
        """
        Creates a thread that will subscribe to spell updates.
        """
        p = self.session.redis.pubsub()
        p.subscribe(
            **{self.spell_update_channel_for_session(self.session.id): subscriber}
        )
        thread = p.run_in_thread(sleep_time=0.001)
        self.listening_threads.append(thread)
        return thread

    def initialize_trigger_times(self) -> None:
        """
        Initialize spell trigger in redis.
        """
        min_time = datetime.now().timestamp()
        trigger_times = {
            0: min_time,
            1: min_time,
            2: min_time,
            3: min_time
        }
        self.store_trigger_times(trigger_times)

    def store_trigger_times(self, trigger_times: dict) -> None:
        """
        Save trigger times dict in redis.
        """
        self.session.redis.hmset(self.key(), trigger_times)

    def load_trigger_times(self) -> dict:
        """
        Loads trigger times dict from redis.
        """
        dict_ = self.session.redis.hgetall(self.key())
        decoded_dict_ = {int(k.decode()): float(v.decode()) for k, v in dict_.items()}
        return decoded_dict_

    def trigger_spell(self, spell_id: int) -> None:
        """
        Updates trigger time of the spell.
        """
        times = self.load_trigger_times()
        assert spell_id in times, spell_id
        times[spell_id] = datetime.now().timestamp()
        self.store_trigger_times(times)

    def is_spell_ready(self, spell_id: int) -> None:
        times = self.load_trigger_times()
        trigger_time = times.get(spell_id)
        trigger_time = datetime.fromtimestamp(trigger_time)
        if trigger_time is None:
            return False
        return datetime.now() - trigger_time > timedelta(seconds=self.COOLDOWN_TIME_PER_SPELL_ID[spell_id])
