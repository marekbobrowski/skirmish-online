from direct.gui.DirectGui import DirectFrame, DGG


class ChatFrame:
    def __init__(self, interface):
        self.interface = interface
        self.node = interface.node.attach_new_node('chat frame node')
        self.frame = None
        self.width = 0.7
        self.height = 0.5
        self.pos = (1, 0, 0.8)

    def load(self):
        self.frame = DirectFrame(
            pos=self.pos,
            parent=self.node,
            frameSize=(0, self.width, -self.height, 0),
            frameColor=(0, 0, 0, 0.5),
            relief=DGG.RAISED,
            borderWidth=(-0.05, 0.1)
        )
