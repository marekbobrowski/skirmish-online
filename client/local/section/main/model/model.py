from protocol.domain.WorldState import WorldState
from client.local.section.main.model.unit import Unit
from client.event import Event
from direct.showbase.DirectObject import DirectObject
from client.local import core


class MainSectionModel(DirectObject):
    def __init__(self):
        DirectObject.__init__(self)
        self.player_id = None
        self.player_unit = None
        self.units_by_id = {}
        self.accept(Event.NEW_UNIT_DATA_RECEIVED, self.handle_new_unit_data_received)
        self.accept(Event.UNIT_POS_ROT_RECEIVED, self.handle_unit_pos_rot_received)
        self.accept(Event.UNIT_HEALTH_RECEIVED, self.handle_unit_health_received)
        self.accept(Event.UNIT_MANA_RECEIVED, self.handle_unit_mana_received)
        self.accept(Event.UNIT_NAME_RECEIVED, self.handle_unit_name_received)
        self.accept(Event.UNIT_ANIMATION_RECEIVED, self.handle_unit_animation_received)
        self.accept(Event.UNIT_MODEL_RECEIVED, self.handle_unit_model_received)
        self.accept(Event.UNIT_WEAPON_RECEIVED, self.handle_unit_weapon_received)
        self.accept(
            Event.MY_ANIMATION_CHANGE_ATTEMPT, self.handle_my_animation_change_attempt
        )
        self.accept(Event.UNIT_DISCONNECTED, self.handle_unit_disconnected)

    def load(self, state: WorldState) -> None:
        self.player_id = state.player.id
        self.player_unit = Unit.from_player(state.player)
        self.units_by_id[self.player_id] = self.player_unit

        if state.other_players is None:
            return

        for other_player in state.other_players.data:
            self.units_by_id[other_player.id] = Unit.from_player(other_player)

    def handle_new_unit_data_received(self, *args):
        unit = args[0]
        self.units_by_id[unit.id] = unit
        core.instance.messenger.send(Event.NEW_UNIT_CREATED, sentArgs=[unit])

    def handle_unit_pos_rot_received(self, *args):
        unit = self.units_by_id[args[0]]
        unit.x = args[1]
        unit.y = args[2]
        unit.z = args[3]
        unit.h = args[4]
        unit.p = args[5]
        unit.r = args[6]
        unit.interpolator.update()
        core.instance.messenger.send(Event.UNIT_POS_ROT_UPDATED, sentArgs=[unit])

    def handle_unit_health_received(self, *args):
        hp_info = args[0]

        for obj in hp_info:
            new_hp = obj.health
            unit_id = obj.id
            unit = self.units_by_id.get(unit_id, None)
            if unit is None:
                continue
            unit.health = new_hp
            core.instance.messenger.send(Event.UNIT_HP_UPDATED, sentArgs=[unit])

    def handle_unit_mana_received(self, *args):
        mana_info = args[0]

        for obj in mana_info:
            new_mana = obj.mana
            unit_id = obj.id
            unit = self.units_by_id.get(unit_id, None)
            if unit is None:
                continue
            unit.mana = new_mana
            core.instance.messenger.send(Event.UNIT_MANA_UPDATED, sentArgs=[unit])

    def handle_unit_name_received(self, *args):
        unit_id, name = args
        unit = self.units_by_id.get(unit_id, None)
        if unit is None:
            return
        unit.name = name
        core.instance.messenger.send(Event.UNIT_NAME_UPDATED, sentArgs=[unit])

    def handle_unit_animation_received(self, *args):
        unit_id, anim, loop = args
        unit = self.units_by_id.get(unit_id, None)
        if unit is None:
            return
        unit.animation = anim
        core.instance.messenger.send(
            Event.UNIT_ANIMATION_UPDATED, sentArgs=[unit, loop]
        )

    def handle_my_animation_change_attempt(self, *args):
        anim, loop = args
        self.player_unit.animation = anim
        core.instance.messenger.send(
            Event.UNIT_ANIMATION_UPDATED, sentArgs=[self.player_unit, loop]
        )

    def handle_unit_model_received(self, *args):
        (
            unit_id,
            model_id,
        ) = args
        unit = self.units_by_id.get(unit_id, None)
        unit.model = model_id
        if unit is None:
            return
        core.instance.messenger.send(Event.UNIT_MODEL_UPDATED, sentArgs=[unit])

    def handle_unit_weapon_received(self, *args):
        unit_id, weapon_id = args
        unit = self.units_by_id.get(unit_id, None)
        if unit is None:
            return
        unit.weapon = weapon_id
        core.instance.messenger.send(Event.UNIT_WEAPON_UPDATED, sentArgs=[unit])

    def handle_unit_disconnected(self, *args):
        unit_id = args[0]
        unit = self.units_by_id.get(unit_id, None)
        unit.actor.delete()
        del unit

    def get_unit_by_name(self, name):
        for unit in self.units_by_id.values():
            if unit.name == name:
                return unit
