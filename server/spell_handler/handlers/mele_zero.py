from .base import BaseSpellHandler
from typing import List
from protocol.domain import Spells


class MeleZeroHandler(BaseSpellHandler):
    SPELL = Spells.mele_zero

    def calculate_targets(self) -> List[int]:
        """
        Calculates targets
        """
        return self.session.player_position_cache.get_nearby(
            self.session.player,
            0.1,
            0.1,
            0.1,
        )

    def interact_with_tagets(self, targets: List[int]) -> int:
        """
        Does action on other targets and calculates hp change
        """
        return 10
