from protocol.domain.WorldState import WorldState
from ...unit import Unit


class MainSectionState:
    def __init__(self):
        self.player_id = None
        self.units_by_id = {}

    def load(self, state: WorldState) -> None:
        self.player_id = state.player.id

        if state.other_players.data is None:
            return

        for other_player in state.other_players.data:
            print(other_player)
