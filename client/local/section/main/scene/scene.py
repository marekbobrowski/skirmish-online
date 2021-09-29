from ..state.state import MainSectionState
from client.local import core

from .skybox import Skybox
from .terrain import Terrain
from .lights import Lights

from .actor_manipulation.manipulator import ActorManipulator


class MainSectionScene:
    def __init__(self, state: MainSectionState):
        self.state = state
        self.node = core.instance.render.attach_new_node("main-section-node")
        self.terrain = Terrain(self.node)
        self.lights = Lights(self.node)
        self.skybox = Skybox(self.node)
        self.manipulator = ActorManipulator(self.state, self.node)

    def show(self) -> None:
        self.node.show()

    def hide(self) -> None:
        self.node.hide()
