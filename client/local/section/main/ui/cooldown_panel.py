from client.local import core
from client.local.font import base
from client.event import Event
from client.local.font import MainFont

from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectFrame, DirectLabel
from direct.task.Task import Task
from panda3d.core import TextNode


class CooldownPanel(DirectObject):
    def __init__(self, node, units):
        DirectObject.__init__(self)
        self.accept("aspectRatioChanged", self.aspect_ratio_change_update)
        self.accept(Event.SET_SPELL_RECEIVED, self.handle_set_spell)
        self.accept(Event.COMBAT_DATA_PARSED, self.handle_combat_data_parsed)
        self.node = node.attach_new_node("combat log node")
        self.units = units

        # --- frame params --- #
        self.width = 0.3
        self.height = 0.5
        frame_color = (0, 0, 0, 0)

        # --- entry & output text params --- #

        # offset from the corner
        self.corner_x_offset = 0.35
        self.corner_y_offset = 0.04

        self.between_line_dist = 0.06

        self.text_scale = 0.02

        # text color/background
        background_color = (0, 0, 0, 1)
        foreground_colors = [
            (0.972, 0.772, 0.745, 1),
            (0.945, 0.972, 0.745, 1),
            (0.8, 0.972, 0.745, 1),
            (0.745, 0.945, 0.972, 1),
            (0.929, 0.745, 0.972, 1),
        ]

        # number of lines displayable in the terminal
        n_lines = 4

        # -- set up console components -- #

        self.frame = DirectFrame(parent=self.node, frameColor=frame_color)

        font = MainFont()
        # font.set_pixels_per_unit(100)

        self.text_nodes = []

        # create node for each line of text, so it can be displaced when resizing the window
        for i in range(n_lines):
            self.text_nodes.append(self.node.attach_new_node(f"text node {i}"))

        # lines of text that are going to be displayed in the terminal
        self.lines = ["" for i in range(n_lines)]

        # (cooldown_time, remaining_time)
        self.cooldowns = [[0, 0] for i in range(n_lines)]

        self.spell_names = ["" for i in range(n_lines)]

        self.direct_labels = []
        for i in range(n_lines):
            self.direct_labels.append(
                DirectLabel(
                    text=self.lines[i],
                    text_align=TextNode.ALeft,
                    text_font=font,
                    text_fg=foreground_colors[i],
                    text_bg=background_color,
                    frameColor=background_color,
                    parent=self.text_nodes[i],
                )
            )
        self.update_view()
        self.set_cooldown_tracking(0, "Spell 1", 1)
        self.set_cooldown_tracking(1, "Spell 2", 2)
        self.set_cooldown_tracking(2, "Spell 3", 3)
        self.set_cooldown_tracking(3, "Spell 4", 4)

    def set_cooldown_tracking(self, slot_number, spell_name, spell_cooldown):
        self.spell_names[slot_number] = spell_name
        self.cooldowns[slot_number] = [spell_cooldown, spell_cooldown]
        task = Task(self.update_cooldown_view, "update cooldown view")
        core.instance.task_mgr.add(task, extraArgs=[task, slot_number, spell_cooldown])

    def handle_set_spell(self, args):
        self.set_cooldown_tracking(
            args.spell_number, args.spell_name, args.spell_cooldown
        )

    def handle_combat_data_parsed(self, *args):
        spell_id = args[0]
        hp_change = args[1]
        if hp_change == 0:
            return

        # trigger cooldown for the spell
        task = Task(self.update_cooldown_view, "update cooldown view")
        core.instance.task_mgr.add(task, extraArgs=[task, spell_id, self.cooldowns[spell_id][0]])

        # trigger global cooldown
        # so that spells aren't used more often than 1 second
        for i in range(len(self.cooldowns)):
            if i != spell_id:
                total, remaining = self.cooldowns[i]
                if remaining < 1:
                    task = Task(self.update_cooldown_view, "update cooldown view")
                    self.cooldowns[i][1] = 1
                    core.instance.task_mgr.add(task, extraArgs=[task, i, 1])

    def update_cooldown_view(self, task, slot_number, cooldown):
        diff = cooldown - task.time
        if diff > 0:
            self.cooldowns[slot_number][1] = diff
            self.zabawny_bogdan(slot_number, cooldown)
            self.update_view()
            return Task.cont
        return Task.done

    def zabawny_bogdan(self, slot_number, cooldown):
        self.lines[slot_number] = (
            self.spell_names[slot_number]
            + " "
            + "|"
            * int(
                (1 - self.cooldowns[slot_number][1] / cooldown)
                * 80
            )
        )

    def aspect_ratio_change_update(self):
        self.frame["frameSize"] = (
            0,
            core.instance.win.get_x_size() * self.width,
            core.instance.win.get_y_size() * -self.height,
            0,
        )
        self.node.set_pos(0, 0, -(1 - self.height) * core.instance.win.get_y_size())
        line_y = 0
        for text_node in reversed(self.text_nodes):
            line_y += self.between_line_dist
            text_node.set_scale(
                (
                    self.text_scale * core.instance.win.get_y_size()
                    + self.text_scale * core.instance.win.get_x_size()
                )
                / 2
            )
            text_node.set_pos(
                self.corner_x_offset * core.instance.win.get_x_size(),
                0,
                -(1 - self.corner_y_offset - line_y)
                * self.height
                * core.instance.win.get_y_size(),
            )

    def update_view(self):
        for i, direct_label in enumerate(self.direct_labels):
            direct_label["text"] = self.lines[i]
