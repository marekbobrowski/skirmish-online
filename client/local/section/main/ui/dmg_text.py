from client.local import core
from client.local.font import MainFont
from client.event import Event

from random import uniform

from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectLabel
from direct.task.Task import Task
from panda3d.core import Vec3


class DmgText(DirectObject):
    MULTIPLY_FACTOR = 412
    """
    We multiply displayed damage for "cooler" effect.
    """

    def __init__(self, units_by_id):
        DirectObject.__init__(self)
        self.units_by_id = units_by_id
        self.accept(Event.COMBAT_DATA_RECEIVED, self.handle_received_combat_data)

        # shaking text settings
        self.init_displacement = 0.2
        self.shake_strength = 0.02
        self.scale_factor = 0.5
        self.floating_up_speed = 0.02
        # XD depending on this value, the scale & trembling is adjusted
        self.big_dmg_assumption = 50

    def handle_received_combat_data(self, *args):
        for target_id in args[3]:
            unit = self.units_by_id.get(target_id, None)
            if unit is not None:
                self.create_randomly_placed_text(unit.base_node, args[1])

    def create_randomly_placed_text(self, node, value):
        font = MainFont()
        text_node = node.attach_new_node("text node")
        text_node.set_pos(
            uniform(-self.init_displacement, self.init_displacement),
            0,
            uniform(self.init_displacement, self.init_displacement),
        )

        scale = 0.15

        text = DirectLabel(
            text=str(value * self.MULTIPLY_FACTOR),
            scale=scale,
            parent=text_node,
            text_bg=(0, 0, 0, 0),
            text_fg=(204, 204, 0, 1),
            frameColor=(0, 0, 0, 0),
            text_font=font,
        )
        text.set_compass(core.instance.camera)
        task = Task(self.shake_and_fade_out_text, "fade out text")
        time = 3
        strength = scale * 0.01
        core.instance.task_mgr.add(
            task, extraArgs=[task, text, text_node, time, strength]
        )

    def shake_and_fade_out_text(self, task, text, text_node, time, strength):
        if task.time < time:
            text_node.set_pos(
                text_node,
                Vec3(
                    uniform(-strength, strength),
                    0,
                    uniform(-strength, strength),
                ),
            )
            text["text_fg"] = (204, 204, 0, 1 - task.time / time)
            text_node.set_z(text_node, self.floating_up_speed)
            text_node.set_pos(
                text_node,
                Vec3(
                    uniform(-strength, strength),
                    0,
                    uniform(-strength, strength),
                ),
            )
            text["text_fg"] = (204, 204, 0, 1 - task.time / time)
            return Task.cont
        else:
            self.destroy_text(text_node)
            return Task.done

    def destroy_text(self, text):
        text.remove_node()
