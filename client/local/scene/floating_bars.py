from local import core
from event import Event
from local import asset_names

from direct.gui.DirectGui import DirectWaitBar, DirectLabel
from direct.showbase.DirectObject import DirectObject


class FloatingBars(DirectObject):
    def __init__(self, characters):
        DirectObject.__init__(self)
        self.characters = characters
        self.bars = {}
        self.labels = {}
        self.accept(Event.PLAYER_JOINED, self.create_bar)
        self.accept(Event.HEALTH_CHANGED, self.update_health)
        self.accept(Event.NAME_CHANGED, self.update_name)

    def update_health(self, id_, health):
        self.bars[id_]['value'] = health

    def update_name(self, id_, name):
        self.labels[id_]['text'] = name

    def create_bar(self, player):
        character = self.characters[player.id]
        new_bar = DirectWaitBar(
            value=player.health,
            pos=(0, 0, 1.5),
            frameColor=(1, 0, 0, 0.3),
            barColor=(0, 1, 0, 1))
        new_bar.reparent_to(character)
        new_bar.set_scale(0.5)
        new_bar.set_compass(core.instance.camera)
        self.bars[player.id] = new_bar

        font = core.instance.loader.load_font(asset_names.main_font)
        new_label = DirectLabel(
            text=player.name,
            pos=(0, 0, 1.57),
            scale=0.14,
            parent=character,
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            text_font=font
        )
        new_label.set_compass(core.instance.camera)
        self.labels[player.id] = new_label
