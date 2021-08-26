from direct.gui.DirectGui import DirectFrame, DGG


class ActionBar:
    def __init__(self, interface):
        self.interface = interface
        self.node = interface.node.attach_new_node("action bar node")
        self.action_frame_size = 0.2
        self.node.set_pos(-2 * self.action_frame_size, 0, -0.7)
        self.skirmish = interface.skirmish
        self.action_frames = []
        self.main_frame = None

    def load(self):
        self.main_frame = DirectFrame(
            parent=self.node,
            frameSize=(0, self.action_frame_size * 4, -self.action_frame_size, 0),
            frameColor=(0, 0, 0, 0.5),
            relief=DGG.RAISED,
            borderWidth=(-0.05, 0.1)
        )

        abilities = self.skirmish.abilities
        for i, icon in enumerate(abilities.icons):
            self.action_frames.append(
                ActionFrame(abilities.names[i], abilities.icons[i],
                            self, (i * self.action_frame_size, 0, 0), self.action_frame_size)
            )

    def update(self):
        for index, frame in enumerate(self.action_frames):
            cd_left = self.skirmish.abilities.cooldowns[index][0]
            cd = self.skirmish.abilities.cooldowns[index][1]
            ratio = cd_left/cd
            frame.update_cooldown(ratio)


class ActionFrame:
    def __init__(self, name, artwork_path, action_bar, pos, size):
        self.name = name
        self.node = action_bar.node.attach_new_node(name + " action frame")
        self.node.set_pos(pos)
        self.size = size
        self.cooldown_frame = DirectFrame(
                parent=self.node,
                pos=(0, 0, 0),
                sortOrder=1,
                frameSize=(0, size, -size, 0),
                frameColor=(0, 0, 0, 0.8)
            )
        self.main_frame = DirectFrame(
                parent=self.node,
                frameSize=(0, size, -size, 0),
                image=artwork_path,
                image_scale=(0.1, 0.1, 0.1),
                sortOrder=0,
                image_pos=(size/2, 0, -size/2)
            ),

    def update_cooldown(self, ratio):
        self.cooldown_frame['frameSize'] = (0, self.size, -self.size * ratio, 0)


