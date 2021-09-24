from protocol.domain.WorldState import WorldState
from client.local.section.main.state.unit import Unit


class MainSectionState:
    def __init__(self):
        self.player_id = None
        self.units_by_id = {}

    def load(self, state: WorldState) -> None:
        self.player_id = state.player.id
        player_unit = Unit.from_player(state.player)
        self.units_by_id[self.player_id] = player_unit

        if state.other_players.data is None:
            return

        for other_player in state.other_players.data:
            self.units_by_id[other_player.id] = Unit.from_player(other_player)
