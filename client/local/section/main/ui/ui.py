from ..model.model import MainSectionModel
from client.local import core
from .console import Console
from .dmg_text import DmgText
from .combat_log import CombatLog
from .cooldown_panel import CooldownPanel
from .floating_bars import FloatingBars


class MainSectionUi:
    def __init__(self, model: MainSectionModel):
        self.model = model
        self.node = core.instance.pixel2d.attach_new_node("interface node")
        self.console = Console(self.node)
        self.dmg_text = DmgText(self.model.units_by_id)
        self.combat_log = CombatLog(self.node, self.model.units_by_id)
        self.cooldown_panel = CooldownPanel(self.node, self.model.units_by_id)
        self.floating_bars = FloatingBars(self.model)

    def show(self) -> None:
        self.node.show()

    def hide(self) -> None:
        self.node.hide()
