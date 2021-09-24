from ..state.state import MainSectionState
from client.local import core
from .console import Console
from .dmg_text import DmgText
from .combat_log import CombatLog
from .cooldown_panel import CooldownPanel


class MainSectionUi:
    def __init__(self, state: MainSectionState):
        self.state = state
        self.node = core.instance.pixel2d.attach_new_node("interface node")
        self.console = Console(self.node)
        self.dmg_text = DmgText(self.state.units_by_id)
        self.combat_log = CombatLog(self.node, self.state.units_by_id)
        self.cooldown_panel = CooldownPanel(self.node, self.state.units_by_id)

    def show(self) -> None:
        self.node.show()

    def hide(self) -> None:
        self.node.hide()
