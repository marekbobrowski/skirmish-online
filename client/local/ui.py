from local import core
from local.console import Console
from local.dmg_text import DmgText


class Ui:
    def __init__(self):
        self.node = core.instance.pixel2d.attach_new_node("interface node")
        self.console = Console(self.node)
        self.dmg_text = DmgText(self.node)
