from direct.gui.DirectGui import DirectFrame, DirectLabel


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
        self.frames['player_frame'] = PlayerFrame(self, "player frame", (-1.2, 0, 0))
        self.frames['target_frame'] = PlayerFrame(self, "target frame", (0.7, 0, 0))

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
        self.length = 0.5
        self.node.set_pos(pos)
        self.frame = DirectFrame(
            parent=self.node,
            frameSize=(0, self.length, -0.5, 0)
        )
        self.sub_frames = {
            'health_frame': DirectFrame(
                parent=self.node,
                pos=(0, 0, -0.1),
                frameSize=(0, self.length, -0.2, 0),
                frameColor=(0.4, 0.1, 0.1, 1)
            ),
            'resource_frame': DirectFrame(
                parent=self.node,
                pos=(0, 0, -0.3),
                frameSize=(0, self.length, -0.2, 0),
                frameColor=(0.1, 0.1, 0.4, 1)
            )
        }
        self.name_label = DirectLabel(
            parent=self.node,
            text='unknown',
            scale=0.1,
            pos=(0.2, 0, -0.05),
            textMayChange=1,
            frameColor=(0, 0, 0, 0)
        )

    def update_health(self, health):
        self.sub_frames.get('health_frame')['frameSize'] = (0, health/100 * self.length, -0.2, 0)

