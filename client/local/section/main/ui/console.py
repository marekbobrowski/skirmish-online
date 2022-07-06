from client.local import core
from client.local.font import MainFont
from client.event import Event
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectFrame, DirectEntry, DirectLabel
from panda3d.core import TextNode
from .command_executor import CommandExecutor
from typing import List
from .utils.frame import Frame, Anchor


class Console(DirectObject):
    def __init__(self, node):
        DirectObject.__init__(self)
        self.node = node.attach_new_node("console node")

        # --- frame params --- #
        self.width = 0.3
        self.height = 0.5
        frame_color = (0, 0, 0, 0)

        # --- entry & output text params --- #

        # offset from the corner
        self.corner_x_offset = 0.04
        self.corner_y_offset = 0.04

        self.between_line_dist = 0.045

        self.text_scale = 0.02

        # text color/background
        background_color = (1, 1, 1, 0)
        foreground_color = (1, 1, 1, 1)

        # number of lines displayable in the terminal
        n_lines = 9

        # distance of the '>' symbol from the entry
        self.input_symbol_offset = 0.0005

        # -- set up console components -- #

        self.frame = Frame(node=node,
                           anchor=Anchor.LEFT_BOTTOM,
                           color=(0, 0, 0, 0.6),
                           x_offset=0.03,
                           y_offset=0.041,
                           width=0.3,
                           height=0.21)

        self.frame.frame.set_bin('fixed', 30)

        #
        font = MainFont()
        font.set_pixels_per_unit(100)

        self.entry_node = self.node.attach_new_node("entry node")
        self.text_nodes = []

        # create node for each line of text, so it can be displaced when resizing the window
        for i in range(n_lines):
            self.text_nodes.append(self.node.attach_new_node(f"text node {i}"))

        # lines of text that are going to be displayed in the terminal
        self.lines_queue = ["" for i in range(n_lines)]

        self.direct_labels = []
        for i in range(n_lines):
            self.direct_labels.append(
                DirectLabel(
                    text=self.lines_queue[i],
                    text_align=TextNode.ALeft,
                    text_font=font,
                    text_fg=foreground_color,
                    text_bg=background_color,
                    frameColor=background_color,
                    parent=self.text_nodes[i],
                )
            )

        self.entry = DirectEntry(
            frameColor=background_color,
            text_fg=foreground_color,
            parent=self.entry_node,
            entryFont=font,
            initialText="",
            width=50,
            command=self.send_msg_event,
            suppressKeys=True,
        )

        self.input_symbol_node = self.entry_node.attach_new_node("input symbol node")
        self.input_symbol = DirectLabel(
            text=">",
            text_align=TextNode.ALeft,
            text_font=font,
            text_fg=foreground_color,
            text_bg=background_color,
            frameColor=background_color,
            parent=self.input_symbol_node,
        )
        self.input_symbol_node.hide()

        self.accept("aspectRatioChanged", self.aspect_ratio_change_update)
        self.accept("enter", self.focus_entry)
        self.accept(Event.MSG_RECEIVED, self.add_msg)
        self.accept(Event.NEW_UNIT_CREATED, self.handle_new_unit_created)

    def handle_new_unit_created(self, *args):
        unit = args[0]
        self.add_msg(name=None, time=None, msg=f"{unit.name} has joined the game.")

    def send_msg_event(self, msg):
        self.input_symbol_node.hide()
        if msg != "":
            self.entry.enterText("")
            self.entry["focus"] = False
            CommandExecutor(msg)()

    def focus_entry(self):
        self.input_symbol_node.show()
        self.entry["focus"] = True

    def aspect_ratio_change_update(self):
        self.node.set_pos(0, 0, -(1 - self.height) * core.instance.win.get_y_size())

        self.entry_node.set_pos(
            self.corner_x_offset * core.instance.win.get_x_size(),
            0,
            -(1 - self.corner_y_offset) * self.height * core.instance.win.get_y_size(),
        )

        self.entry_node.set_scale(
            (
                self.text_scale * core.instance.win.get_y_size()
                + self.text_scale * core.instance.win.get_x_size()
            )
            / 2
        )

        self.input_symbol_node.set_x(
            -self.input_symbol_offset * core.instance.win.get_x_size()
        )

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

    def add_msg(self, name, time, msg):
        if name is None:
            lines = msg.splitlines()
        else:
            lines = [f"[{time}] {name}: {msg}"]
        for line in lines:
            self.add_lines(self.split_into_smaller_lines(line, chars_per_line=40))
        self.update_view()

    def split_into_smaller_lines(self, string: str, chars_per_line: int) -> List[str]:
        return [string[i:i+chars_per_line] for i in range(0, len(string), chars_per_line)]

    def add_lines(self, lines):
        """
        :param lines: array of lines to be added
        """
        for line in lines:
            self.lines_queue.append(line)
            self.lines_queue.pop(0)

    def update_view(self):
        for i, direct_label in enumerate(self.direct_labels):
            direct_label["text"] = self.lines_queue[i]
