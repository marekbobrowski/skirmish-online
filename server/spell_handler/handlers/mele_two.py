from .base import BaseSpellHandler
from typing import List
from protocol.domain import Spells, AnimationName
import random


class MeleTwoHandler(BaseSpellHandler):
    SPELL = Spells.mele_two
    ANIMATION = AnimationName.MagicAttack1

    def calculate_targets(self) -> List[int]:
        """
        Calculates targets
        """
        return self.session.player_position_cache.get_nearby(
            self.session.player,
            0.4,
            0.4,
            0.4,
        )

    def interact_with_tagets(self, targets: List[int]) -> int:
        """
        Does animation on other targets and calculates hp change
        """
        return random.randint(26, 31)
