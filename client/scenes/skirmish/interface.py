from scenes.skirmish.quick_menu import QuickMenu
from direct.task.Task import Task
from scenes.skirmish.player_frames import PlayerFrames


class Interface:
    def __init__(self, skirmish):
        self.skirmish = skirmish
        self.core = skirmish.core
        self.node = skirmish.node_2d.attach_new_node("skirmish interface node")
        self.submodules = [QuickMenu(self), PlayerFrames(self)]

    def load(self):
        self.submodules[0].node.hide()
        for submodule in self.submodules:
            submodule.load()

    def update(self, task):
        self.submodules[1].update()
        return Task.cont
