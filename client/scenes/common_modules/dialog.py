from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton


class Dialog:
    def __init__(self, parent, frame_size, label, button_label, function):
        self.node = parent.attach_new_node("dialog node")
        self.frame = DirectFrame(parent=self.node,
                                 frameSize=frame_size)
        self.label = DirectLabel(parent=self.node,
                                 text_scale=0.1,
                                 text=label)
        self.button = DirectButton(parent=self.node,
                                   text=button_label,
                                   command=function,
                                   scale=0.1,
                                   pos=(0, 0, -0.1))

    def set_button(self, text, function):
        pass

    def set_label(self, text):
        self.label.setText(text)

    def show(self):
        self.node.show()

    def hide(self):
        self.node.hide()



