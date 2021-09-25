from . import core, asset_names
from ..event import Event

from direct.gui.DirectGui import DirectWaitBar, DirectLabel
from direct.showbase.DirectObject import DirectObject


class FloatingBars(DirectObject):
    def __init__(self, units):
        DirectObject.__init__(self)
        self.units = units
        self.bars = {}
        self.labels = {}
        self.accept(Event.PLAYER_JOINED, self.handle_player_joined)
        self.accept(Event.HEALTH_CHANGED, self.update_health)
        self.accept(Event.NAME_CHANGED, self.update_name)

    def handle_player_joined(self, args):
        unit = self.units.get(args.unit.id, None)
        if unit is not None:
            self.create_bar(unit)

    def update_health(self, id_, health):
        bar = self.bars.get(id_, None)
        if bar is not None:
            bar["value"] = health

    def update_name(self, id_, name):
        label = self.labels.get(id_, None)
        if label is not None:
            label["text"] = name

    def create_bar(self, unit):
        _ = self.units[unit.id].actor
        unit = self.units[unit.id]
        new_bar = DirectWaitBar(
            value=unit.health,
            pos=(0, 0, 0.5),
            frameColor=(1, 0, 0, 0.3),
            barColor=(0, 1, 0, 1),
        )
        new_bar.reparent_to(unit.base_node)
        new_bar.set_scale(0.13)
        new_bar.set_compass(core.instance.camera)
        self.bars[unit.id] = new_bar

        font = core.instance.loader.load_font(asset_names.main_font)
        new_label = DirectLabel(
            text=unit.name,
            pos=(0, 0, 0.53),
            scale=0.04,
            parent=unit.base_node,
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            text_font=font,
        )
        new_label.set_compass(core.instance.camera)
        self.labels[unit.id] = new_label
