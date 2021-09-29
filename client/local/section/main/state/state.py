from protocol.domain.WorldState import WorldState
from client.local.section.main.state.unit import Unit
from client.net.server_event import ServerEvent
from client.local.client_event import ClientEvent
from direct.showbase.DirectObject import DirectObject
from client.local import core


class MainSectionState(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)
        self.player_id = None
        self.player_unit = None
        self.units_by_id = {}
        self.accept(ServerEvent.PLAYER_JOINED, self.handle_player_joined)
        self.accept(ServerEvent.HEALTH_CHANGED, self.handle_health_changed)
        self.accept(
            ServerEvent.PLAYER_CHANGED_POS_HPR, self.handle_player_changed_pos_hpr
        )

    def load(self, state: WorldState) -> None:
        self.player_id = state.player.id
        self.player_unit = Unit.from_player(state.player)
        self.units_by_id[self.player_id] = self.player_unit

        if state.other_players is None:
            return

        for other_player in state.other_players.data:
            self.units_by_id[other_player.id] = Unit.from_player(other_player)

    def handle_player_joined(self, *args):
        unit = args[0]
        self.units_by_id[unit.id] = unit
        core.instance.messenger.send(ClientEvent.NEW_UNIT, sentArgs=[unit])

    def handle_health_changed(self, *args):
        hp_info = args[0]

        for obj in hp_info:
            new_hp = obj.health
            unit_id = obj.id

            unit = self.units_by_id[unit_id]
            unit.health = new_hp

            core.instance.messenger.send(ClientEvent.UNIT_HP, sentArgs=[unit, new_hp])

    def handle_player_changed_pos_hpr(self, *args):
        unit = self.units_by_id[args[0]]
        unit.x = args[1]
        unit.y = args[2]
        unit.z = args[3]
        unit.h = args[4]
        unit.p = args[5]
        unit.r = args[6]
        unit.interpolator.update()
        core.instance.messenger.send(ClientEvent.UNIT_POS_ROT, sentArgs=[unit])
