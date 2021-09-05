from local import core
from event import Event
from local import asset_names

from direct.gui.DirectGui import DirectWaitBar, DirectLabel
from panda3d.core import TextNode


class FloatingBars:
    def __init__(self, characters):
        self.characters = characters
        self.bars = []
        core.instance.accept(Event.HEALTH_CHANGED, self.update_health)
        core.instance.accept(Event.PLAYER_JOINED, self.create_bar)
        core.instance.accept(Event.NAME_CHANGED, self.update_name)

    def update_health(self, player):
        self.bars[player.id]['value'] = player.health

    def update_name(self, player):
        self.bars[player.id]['text'] = player.name

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

        font = core.instance.loader.load_font(asset_names.main_font)
        new_label = DirectLabel(
            text=player.name,
            pos=(0, 0, 1.57),
            scale=0.14,
            parent=player.character,
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            text_font=font
        )
        new_label.set_compass(core.instance.camera)
