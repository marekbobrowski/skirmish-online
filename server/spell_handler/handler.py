from protocol.domain import CombatData
import logging

log = logging.getLogger(__name__)


class SpellHandler:
    def __init__(self, spell_data, session):
        """
        Handling of upcoming spells is done here, in this class.

        Implement veryfication, spell distinguish etc here.
        """
        self.spell_data = spell_data
        self.session = session

    def __call__(self) -> CombatData:
        """
        This is the main procedure. Hadles the spell, and produces
        CombatData packet that is distrubuted to original client.

        Additionally, publishing spell information should be done
        here
        """
        log.info(self.spell_data.__dict__)
        # return CombatData(1, 1, 1, [1])
