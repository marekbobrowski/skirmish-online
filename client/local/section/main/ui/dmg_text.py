from client.local import core
from client.local.assets import asset_names as assets
from client.event import Event

from random import uniform

from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectLabel
from direct.task.Task import Task
from panda3d.core import Vec3


class DmgText(DirectObject):
    def __init__(self, units):
        DirectObject.__init__(self)
        self.units = units
        self.accept(Event.RECEIVED_COMBAT_DATA, self.handle_received_combat_data)

    def handle_received_combat_data(self, args):
        for target_id in args.target_ids:
            unit = self.units.get(target_id, None)
            if unit is not None:
                self.create_randomly_placed_text(unit.base_node, -args.hp_change)

    def create_randomly_placed_text(self, node, value):
        font = core.instance.loader.load_font(assets.main_font)
        text_node = node.attach_new_node("text node")
        text_node.set_pos(uniform(-0.3, 0.3), 0, uniform(0.6, 0.65))
        text = DirectLabel(
            text=str(value),
            scale=0.2 * value / 10000,
            parent=text_node,
            text_bg=(0, 0, 0, 0),
            text_fg=(204, 204, 0, 1),
            frameColor=(0, 0, 0, 0),
            text_font=font,
        )
        text.set_compass(core.instance.camera)
        task = Task(self.shake_and_fade_out_text, "fade out text")
        time = 5 * value / 10000
        strength = 0.4 * value / 10000
        core.instance.task_mgr.add(
            task, extraArgs=[task, text, text_node, time, strength]
        )
        # core.instance.add_task(self.destroy_text)
        # core.instance.task_mgr.do_method_later(0.5, self.destroy_text, 'destroy text', extraArgs=[text])

    def shake_and_fade_out_text(self, task, text, text_node, time, strength):
        if task.time < time:
            text_node.set_pos(
                text_node,
                Vec3(
                    uniform(-0.01 * strength, 0.01 * strength),
                    0,
                    uniform(-0.01 * strength, 0.01 * strength),
                ),
            )
            text["text_fg"] = (204, 204, 0, 1 - task.time / time)
            text_node.set_z(text_node, 0.006)
            text_node.set_pos(
                text_node,
                Vec3(
                    uniform(-0.01 * strength, 0.01 * strength),
                    0,
                    uniform(-0.01 * strength, 0.01 * strength),
                ),
            )
            text["text_fg"] = (204, 204, 0, 1 - task.time / time)
            text_node.set_z(text_node, 0.001)
            return Task.cont
        else:
            self.destroy_text(text_node)
            return Task.done

    def destroy_text(self, text):
        text.remove_node()
