from .state.state import MainSectionState
from .scene.scene import MainSectionScene
from .control.control import Control
from .ui.ui import MainSectionUi
from ..base import Section
from protocol.domain.WorldState import WorldState
from client.local import core
from .state.node_watcher import NodeWatcher


class MainSection(Section):
    def __init__(self):
        self.state = MainSectionState()
        self.scene = MainSectionScene(self.state)
        self.ui = MainSectionUi(self.state)
        self.control = None

    def show(self) -> None:
        self.scene.show()
        self.ui.show()

    def hide(self) -> None:
        self.scene.hide()
        self.ui.hide()

    def load_state(self, state: WorldState) -> None:
        self.state.load(state)

    def post_state_setup(self) -> None:
        units = self.state.units_by_id.values()
        for unit in units:
            self.scene.manipulator.spawn_unit(unit)
            self.ui.floating_bars.create_bar(unit)
        self.enable_control()
        NodeWatcher(self.state.player_unit.base_node, self.scene.node, 0).enable()

    def enable_control(self) -> None:
        player_unit = self.state.units_by_id[self.state.player_id]
        self.control = Control(player_unit, core.instance.camera)
        self.control.enable(self.scene.node)

    def disable_control(self) -> None:
        pass
