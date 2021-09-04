from local import core
from event import Event
from local import asset_names

from direct.gui.DirectGui import DirectWaitBar, DirectLabel
from panda3d.core import TextNode


class FloatingBars:
    def __init__(self, world):
        self.world = world
        self.bars = []
        core.instance.accept(Event.HEALTH_CHANGED, self.update_health)
        core.instance.accept(Event.PLAYER_JOINED, self.create_bar)
        core.instance.accept(Event.NAME_CHANGED, self.update_name)

    def update_health(self, player):
        player.health_bar['value'] = player.health

    def update_name(self, player):
        player.name_label['text'] = player.name

    def create_bar(self, player):
        player.health_bar = DirectWaitBar(
            value=player.health,
            pos=(0, 0, 1.5),
            frameColor=(1, 0, 0, 0.3),
            barColor=(0, 1, 0, 1))

        player.health_bar.reparent_to(player.character)
        player.health_bar.set_scale(0.5)
        player.health_bar.set_compass(core.instance.camera)

        font = core.instance.loader.load_font(asset_names.terminal_style)
        player.name_label = DirectLabel(
            text=player.name,
            pos=(0, 0, 1.57),
            scale=0.14,
            parent=player.character,
            text_bg=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
            frameColor=(0, 0, 0, 0),
            text_font=font
        )
        player.name_label.set_compass(core.instance.camera)
