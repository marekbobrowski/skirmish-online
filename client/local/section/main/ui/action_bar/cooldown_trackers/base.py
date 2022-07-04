from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectWaitBar
from client.local.section.main.ui.utils.frame import Frame
from client.local.section.main.ui.utils.wait_bar import WaitBar
from direct.task.Task import Task


class CooldownTrackerBase(DirectObject):
    ICON = None

    def __init__(self, node, x_offset, y_offset, parent_frame=None):
        DirectObject.__init__(self)
        self.node = node.attach_new_node("action bar")
        if self.ICON is None:
            color = (0, 0, 0, 1)
        else:
            color = (1, 1, 1, 1)
        self.frame = Frame(node=self.node,
                           anchor=None,
                           color=color,
                           x_offset=x_offset,
                           y_offset=y_offset,
                           width=0.026,
                           height=0.046,
                           scale=1000,
                           parent_frame=parent_frame,
                           hpr=(0, 0, 180),
                           image=self.ICON)

        self.cd_bar = WaitBar(parent=self.frame.node)
        self.default_cooldown = 1
        self.remaining_time = 0

    def update_cooldown_view(self, task, cooldown):
        diff = cooldown - task.time
        if diff > 0:
            self.remaining_time = diff
            self.update_view(diff, cooldown)
            return Task.cont
        return Task.done

    def update_view(self, remaining_time, cooldown):
        xd = 1 - remaining_time / cooldown
        self.cd_bar.wait_bar["value"] = xd * 100


