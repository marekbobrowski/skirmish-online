from direct.gui.DirectGui import DirectFrame, DirectEntry, DirectLabel, DGG


class ChatFrame:
    def __init__(self, interface):
        self.interface = interface
        self.skirmish = interface.skirmish
        self.node = interface.node.attach_new_node('chat frame node')
        self.max_chars_in_line = 20
        self.pos = (1, 0, 0.8)
        self.node.set_pos(self.pos)
        self.frame = None
        self.entry = None
        self.width = 0.7
        self.height = 0.5
        self.focused = False
        self.chat_text = None

    def load(self):
        self.frame = DirectFrame(
            parent=self.node,
            frameSize=(0, self.width, -self.height, 0),
            frameColor=(0, 0, 0, 0.5),
            relief=DGG.RAISED,
            borderWidth=(-0.05, 0.1)
        )
        self.entry = DirectEntry(scale=0.1,
                                 pos=(0, 0, -self.height),
                                 frameColor=(0.7, 0.7, 0.7, 0.4),
                                 width=7,
                                 relief=DGG.RIDGE,
                                 parent=self.node)
        self.chat_text = DirectLabel(parent=self.node,
                                     pos=(0.2, 0, 0),
                                     text='',
                                     scale=0.05)

    def focus(self):
        self.focused = True
        self.entry['focus'] = True

    def remove_focus(self):
        self.focused = False
        self.entry['focus'] = False
        self.entry.enterText('')

    def add_message(self, name, message):
        self.chat_text['text'] = self.chat_text['text'] + "\n" + name + ": " + message