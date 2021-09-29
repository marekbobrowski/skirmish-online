from client.local import core
from client.local.assets import asset_names as assets
from client.net.server_event import ServerEvent
from client.local.client_event import ClientEvent
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectFrame, DirectEntry, DirectLabel
from panda3d.core import TextNode
from . import command


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
        n_lines = 40

        # distance of the '>' symbol from the entry
        self.input_symbol_offset = 0.0005

        # -- set up console components -- #

        self.frame = DirectFrame(parent=self.node, frameColor=frame_color)

        font = core.instance.loader.load_font(assets.main_font)
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
        self.accept(ServerEvent.TXT_MSG_FROM_SERVER_RECEIVED, self.add_msg)

    def send_msg_event(self, msg):
        self.input_symbol_node.hide()
        if msg != "":
            self.entry.enterText("")
            self.entry["focus"] = False
            core.instance.messenger.send(event=ClientEvent.COMMAND, sentArgs=[msg])

    def focus_entry(self):
        self.input_symbol_node.show()
        self.entry["focus"] = True

    def aspect_ratio_change_update(self):
        self.frame["frameSize"] = (
            0,
            core.instance.win.get_x_size() * self.width,
            core.instance.win.get_y_size() * -self.height,
            0,
        )
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
            self.add_lines(msg.splitlines())
        else:
            self.add_lines([f"[{time}] {name}: {msg}"])
        self.update_view()

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
