from direct.gui.DirectGui import DirectFrame, DirectLabel, DGG


# noinspection PyTypeChecker
class PlayerFrames:
    def __init__(self, interface):
        self.interface = interface
        self.skirmish = interface.skirmish
        self.node = interface.node.attach_new_node("player frames node")
        self.frames = {
            'player_frame': None,
            'target_frame': None
        }

    def load(self):
        self.frames['player_frame'] = PlayerFrame(self, "player frame", (-1.5, 0, -0.6))
        self.frames['target_frame'] = PlayerFrame(self, "target frame", (0.5, 0, -0.6))

    def update(self):
        self.frames.get('player_frame').name_label.setText(self.skirmish.player.name)
        self.frames.get('player_frame').update_health(self.skirmish.player.health)
        if self.skirmish.player.target is not None:
            self.frames.get('target_frame').node.show()
            self.frames.get('target_frame').name_label.setText(self.skirmish.player.target.name)
            self.frames.get('target_frame').update_health(self.skirmish.player.target.health)
        else:
            self.frames.get('target_frame').node.hide()


class PlayerFrame:
    def __init__(self, player_frames, frame_name, pos):
        self.node = player_frames.node.attach_new_node(frame_name)
        self.length = 1
        self.height = 0.2
        self.bar_scale = 0.22
        self.text_bar_scale = 1 - 2 * self.bar_scale
        self.node.set_pos(pos)
        self.frame = DirectFrame(
            parent=self.node,
            frameSize=(0, self.length, -self.height, 0),
            frameColor=(0, 0, 0, 0.5),
            relief=DGG.RAISED,
            borderWidth=(-0.05, 0.1)
        )
        self.sub_frames = {
            'health_frame': DirectFrame(
                parent=self.node,
                pos=(0, 0, - self.text_bar_scale * self.height),
                frameSize=(0, self.length, -self.height * self.bar_scale, 0),
                frameColor=(0.4, 0.1, 0.1, 1)
            ),
            'resource_frame': DirectFrame(
                parent=self.node,
                pos=(0, 0, (-self.text_bar_scale-self.bar_scale)*self.height),
                frameSize=(0, self.length, -self.height * self.bar_scale, 0),
                frameColor=(0.1, 0.1, 0.4, 1)
            )
        }
        self.name_label = DirectLabel(
            parent=self.node,
            text='unknown',
            scale=0.1,
            pos=(0.5, 0, -0.08),
            textMayChange=1,
            frameColor=(0, 0, 0, 0),
            text_fg=(0.9, 0.9, 0.9, 1)
        )

    def update_health(self, health):
        self.sub_frames.get('health_frame')['frameSize'] = (0, health/100 * self.length,
                                                            -self.height * self.bar_scale, 0)

