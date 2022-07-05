from client.local import core
from client.event import Event
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectFrame, DirectEntry, DirectLabel, DGG
from panda3d.core import TextNode
from client.local.font import MainFont


class Anchor:
    CENTER = "center_bottom"
    LEFT_BOTTOM = "left_bottom"


class Frame(DirectObject):
    """
    Wrapper for DirectFrame that scales/moves accordingly to the window size (for Pixel2d root).
    """
    def __init__(self, node, anchor, color, x_offset, y_offset, width, height, parent_frame=None, image=None, hpr=(0,0,0), image_hpr=(0,0,0), scale=1, text=""):
        DirectObject.__init__(self)
        self.anchor = anchor
        self.node = node.attach_new_node(f"frame {self}")
        self.text_x_offset = 0.004
        self.text_y_offset = 0.016
        self.text_scale = 0.01
        self.frame = DirectFrame(
            hpr=hpr,
            parent=self.node,
            frameColor=color,
            frameTexture=image,
            image_hpr=image_hpr,
            text=text,
            text_roll=180,
            text_scale=20,
            text_font=MainFont(),
            text_fg=(1, 1, 1, 1),
        )
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height
        self.accept("aspectRatioChanged", self.aspect_ratio_change_update)
        self.parent_frame = parent_frame

    def aspect_ratio_change_update(self):
        """
        Rescale/move frame when the window size has changed.
        """

        if self.parent_frame is None:
            reference_width = core.instance.win.get_x_size()
            reference_height = core.instance.win.get_y_size()
        else:
            print('halo')
            reference_width = self.parent_frame.get_x_size()
            print(reference_width)
            reference_height = self.parent_frame.get_y_size()

        center = reference_width / 2
        width_px = reference_width * self.width
        height_px = reference_height * self.height
        self.frame["frameSize"] = (
            0,
            width_px,
            height_px,
            0,
        )
        self.frame["text_pos"] = (reference_width * self.text_x_offset, reference_height * self.text_y_offset, 0)
        self.frame["text_scale"] = reference_width * self.text_scale
        if self.anchor == Anchor.CENTER:
            self.node.set_pos(center - width_px / 2, 0, -reference_height * (1 - self.y_offset))
        elif self.anchor == Anchor.LEFT_BOTTOM:
            self.node.set_pos(reference_width * self.x_offset, 0, -reference_height * (1 - self.y_offset))
        elif self.anchor is None:
            self.node.set_pos(reference_width * self.x_offset, 0, reference_height * self.y_offset)

    def get_x_size(self):
        return self.frame["frameSize"][1]

    def get_y_size(self):
        return self.frame["frameSize"][2]



