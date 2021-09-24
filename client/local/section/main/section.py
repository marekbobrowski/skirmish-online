from .state import MainSectionState
from .scene import MainSectionScene
from .ui import MainSectionUi
from ..base import Section
from protocol.domain.WorldState import WorldState


class MainSection(Section):
    def __init__(self):
        self.state = MainSectionState()
        self.scene = MainSectionScene(self.state)
        self.ui = MainSectionUi(self.state)

    def enter(self) -> None:
        self.scene.show()
        self.ui.show()

    def leave(self) -> None:
        self.scene.hide()
        self.ui.hide()

    def load_state(self, state: WorldState) -> None:
        self.state.load(state)

    # self.world = World()
    # self.ui = Ui(self.world.units)
    #
    # self.net_client.load_world_state(self.world)
    # self.net_client.send_ready_for_updates()
    #
    # main_player = self.world.units[self.world.main_player_id]
    # control = Control(main_player, core.instance.camera)
    # control.enable(self.world.node)
    # self.net_client.begin_sync(main_player.base_node, self.world.node)
    # core.instance.run()
    # # print("Connecting...")
    # # if self.net_client.connect(server_ip):
    # #     print("Connected. Loading assets...")
    #
    # # load_assets_to_cache()