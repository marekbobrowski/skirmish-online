from protocol.domain.WorldState import WorldState
from client.local.section.main.state.unit import Unit
from client.event import Event
from direct.showbase.DirectObject import DirectObject
from client.local import core


class MainSectionState(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)
        self.player_id = None
        self.units_by_id = {}
        self.accept(Event.PLAYER_JOINED, self.handle_player_joined)

    def load(self, state: WorldState) -> None:
        self.player_id = state.player.id
        player_unit = Unit.from_player(state.player)
        self.units_by_id[self.player_id] = player_unit

        if state.other_players is None:
            return

        for other_player in state.other_players.data:
            self.units_by_id[other_player.id] = Unit.from_player(other_player)

    def handle_player_joined(self, *args):
        unit = args[0]
        self.units_by_id[unit.id] = unit
        core.instance.messenger.send(Event.LOCAL_NEW_UNIT, sentArgs=[unit])
