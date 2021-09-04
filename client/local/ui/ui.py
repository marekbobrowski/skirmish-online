from local import core
from local.ui.console import Console
from local.ui.floating_bars import FloatingBars


class Ui:
    def __init__(self, interlocutor, world):
        self.node = core.instance.pixel2d.attach_new_node("interface node")
        self.world = world
        self.console = Console(self.node, interlocutor)
        self.floating_bars = FloatingBars(world)

