from local import core
from local.console import Console
from local.combat_log import CombatLog


class Ui:
    def __init__(self, units):
        self.node = core.instance.pixel2d.attach_new_node("interface node")
        self.console = Console(self.node)
        self.combat_log = CombatLog(self.node, units)
