from ...storage.domain.combat_data import CombatData
from protocol.domain import Spells, AnimationName, Animation
from .bank import MetaClass
from abc import abstractmethod
from typing import List


class BaseSpellHandler(metaclass=MetaClass):
    SPELL: Spells = None
    ANIMATION: AnimationName = None
    LOOP: int = 0

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
        if not self.valid():
            return

        self.publish_spell_update()
        self.publish_animation_update()
        targets = self.calculate_targets()
        hp_change = self.interact_with_tagets(targets)
        self.publish_health_update(targets, hp_change)
        self.session.player_cache.publish_mana_update([self.session.player.id], 5)
        return self.produce_response(targets, hp_change)

    def valid(self) -> bool:
        """
        If spell is valid
        """
        return True

    def publish_spell_update(self):
        """
        Notifies all other players about
        spell being casted
        """
        self.session.spell_cache.publish_spell_update(self.spell_data)

    def publish_animation_update(self):
        """
        Notifies all other players about
        new animation
        """
        self.session.set_animation(
            Animation(animation_name=self.ANIMATION.value, loop=self.LOOP),
        )

    def publish_health_update(self, targets, hp_change):
        """
        Notifies all other players about
        health updates
        """
        self.session.player_cache.publish_health_update(
            targets,
            hp_change,
        )

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
