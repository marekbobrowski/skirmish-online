from . import core
from .console import Console
from .combat_log import CombatLog
from .dmg_text import DmgText
from .cooldown_panel import CooldownPanel


class Ui:
    def __init__(self, units):
        self.node = core.instance.pixel2d.attach_new_node("interface node")
        self.console = Console(self.node)
        self.dmg_text = DmgText(units)
        self.combat_log = CombatLog(self.node, units)
        self.cooldown_panel = CooldownPanel(self.node, units)
