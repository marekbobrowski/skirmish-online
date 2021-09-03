from local import core
from local.ui.console import Console


class Ui:
    def __init__(self, interlocutor):
        self.node = core.instance.pixel2d.attach_new_node("interface node")
        self.console = Console(self.node, interlocutor)
