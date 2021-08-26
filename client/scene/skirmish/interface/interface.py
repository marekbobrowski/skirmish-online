from scene.skirmish.interface.quick_menu import QuickMenu
from direct.task.Task import Task
from scene.skirmish.interface.player_frames import PlayerFrames
from scene.skirmish.interface.action_bar import ActionBar
from scene.skirmish.interface.chat_frame import ChatFrame
from scene.skirmish.interface.score_board import ScoreBoard


class Interface:
    def __init__(self, skirmish):
        self.skirmish = skirmish
        self.node = skirmish.node_2d.attach_new_node("skirmish interface node")
        self.submodules = [QuickMenu(self), PlayerFrames(self), ActionBar(self), ChatFrame(self),
                           ScoreBoard(self)]

    def load(self):
        self.submodules[0].node.hide()
        for submodule in self.submodules:
            submodule.load()

    def update(self, task):
        # self.submodules[1].update()
        # self.submodules[2].update()
        return Task.cont
