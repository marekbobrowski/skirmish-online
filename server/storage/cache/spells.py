from ..domain import SpellUpdate
from server.event.event_user import EventUser
import json
import dataclasses


class SpellCache(EventUser):
    SPELL_UPDATE_CHANNEL = "spell_update_"

    def __init__(self, session):
        super().__init__()
        self.session = session

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
