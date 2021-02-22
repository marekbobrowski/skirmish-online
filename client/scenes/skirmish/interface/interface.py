from scenes.skirmish.interface.quick_menu import QuickMenu
from direct.task.Task import Task
from scenes.skirmish.interface.player_frames import PlayerFrames
from scenes.skirmish.interface.action_bar import ActionBar


class Interface:
    def __init__(self, skirmish):
        self.skirmish = skirmish
        self.core = skirmish.core
        self.node = skirmish.node_2d.attach_new_node("skirmish interface node")
        self.submodules = [QuickMenu(self), PlayerFrames(self), ActionBar(self)]

    def load(self):
        self.submodules[0].node.hide()
        for submodule in self.submodules:
            submodule.load()

    def update(self, task):
        self.submodules[1].update()
        self.submodules[2].update()
        return Task.cont
