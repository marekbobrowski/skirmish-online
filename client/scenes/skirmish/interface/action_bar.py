from direct.gui.DirectGui import DirectFrame


class ActionBar:
    def __init__(self, interface):
        self.interface = interface
        self.node = interface.node.attach_new_node("action bar node")
        self.node.set_pos(-1.2, 0, -0.5)
        self.skirmish = interface.skirmish
        self.core = interface.core
        self.action_frames = []

        self.action_frame_size = 0.2

    def load(self):
        player_class = self.skirmish.player.player_class
        for i, action in enumerate(player_class.actions):
            self.action_frames.append(
                ActionFrame(action[0], action[2], self, (i * self.action_frame_size, 0, 0), self.action_frame_size)
            )

    def update(self):
        pass


class ActionFrame:
    def __init__(self, name, artwork_path, action_bar, pos, size):
        self.name = name
        self.node = action_bar.node.attach_new_node(name + " action frame")
        self.node.set_pos(pos)
        self.main_frame = DirectFrame(
                parent=self.node,
                frameSize=(0, size, -size, 0),
                image=artwork_path,
                image_scale=(0.1, 0.1, 0.1),
                image_pos=(size/2, 0, -size/2)
            ),
