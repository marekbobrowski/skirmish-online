from client.local import core
from client.local.assets import asset_names
from client.event import Event

from ..model.model import MainSectionModel

from direct.gui.DirectGui import DirectWaitBar, DirectLabel
from direct.showbase.DirectObject import DirectObject


class FloatingBars(DirectObject):
    def __init__(self, model: MainSectionModel):
        DirectObject.__init__(self)
        self.model = model
        self.bars = {}
        self.labels = {}
        self.accept(Event.NEW_UNIT_CREATED, self.handle_local_new_unit)
        self.accept(Event.UNIT_HP_UPDATED, self.handle_unit_hp_updated)
        self.accept(Event.UNIT_NAME_UPDATED, self.handle_unit_name_updated)
        self.accept(Event.UNIT_DISCONNECTED, self.handle_unit_disconnected)

    def handle_local_new_unit(self, *args):
        unit = args[0]
        if unit is not None:
            self.create_bar(unit)

    def handle_unit_hp_updated(self, *args):
        unit = args[0]
        self.update_health_bar(unit)

    def handle_unit_name_updated(self, *args):
        unit = args[0]
        self.update_name_label(unit)

    def handle_unit_disconnected(self, *args):
        unit_id = args[0]
        self.delete_label_and_bar(unit_id)

    def delete_label_and_bar(self, unit_id):
        bar = self.bars.get(unit_id, None)
        label = self.labels.get(unit_id, None)
        if bar is not None:
            bar.destroy()
            del self.bars[unit_id]
        if label is not None:
            label.destroy()
            del self.labels[unit_id]

    def update_health_bar(self, unit):
        bar = self.bars.get(unit.id, None)
        if bar is not None:
            bar["value"] = unit.health

    def update_name_label(self, unit):
        label = self.labels.get(unit.id, None)
        if label is not None:
            label["text"] = unit.name

    def create_bar(self, unit):
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
