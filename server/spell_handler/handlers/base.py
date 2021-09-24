from ...storage.domain.combat_data import CombatData
from .bank import MetaClass
from abc import abstractmethod
from typing import List


class BaseSpellHandler(metaclass=MetaClass):
    SPELL: int = None

    def __init__(self, session, spell_data):
        """
        Stores session and spell data
        """
        self.session = session
        self.spell_data = spell_data

    def __call__(self) -> CombatData:
        """
        Main method. It does several things:
            1. publish_spell_update
            2. calculate_targets
            3. interact with targets
            4. produce response
        """
        self.publish_spell_update()
        targets = self.calculate_targets()
        hp_change = self.interact_with_tagets(targets)
        return self.produce_response(targets, hp_change)

    def publish_spell_update(self):
        """
        Notifies all other players about
        spell being casted
        """
        self.session.spell_cache.publish_spell_update(self.spell_data)

    @abstractmethod
    def calculate_targets(self) -> List[int]:
        """
        Calculates targets
        """
        pass

    @abstractmethod
    def interact_with_tagets(self, targets: List[int]) -> int:
        """
        Does action on other targets and calculates hp change
        """
        pass

    def produce_response(self, targets: List[int], hp_change: int) -> CombatData:
        """
        Produces response
        """
        return CombatData(
            spell=self.spell_data.spell,
            hp_change=hp_change,
            source=self.session.player.id,
            targets=targets,
        )
