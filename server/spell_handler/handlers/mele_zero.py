from .base import BaseSpellHandler
from typing import List
from protocol.domain import Spells


class MeleZeroHandler(BaseSpellHandler):
    SPELL = Spells.mele_zero

    def calculate_targets(self) -> List[int]:
        """
        Calculates targets
        """
        return list(self.session.player_cache.other_player_ids())

    def interact_with_tagets(self, targets: List[int]) -> int:
        """
        Does action on other targets and calculates hp change
        """
        return 10
