from direct.gui.DirectGui import DirectButton
import sys
from direct.task.Task import Task


class QuickMenu:
    def __init__(self, interface):
        self.interface = interface
        self.core = interface.core
        self.node = interface.node.attach_new_node("quick menu node")

        self.return_btn = None
        self.audio_btn = None
        self.leave_skirmish_btn = None
        self.exit_game_btn = None
        self.visible = False

    def enter(self):
        self.node.show()

    def leave(self):
        self.node.hide()

    def toggle(self):
        self.visible = not self.visible
        self.enter() if self.visible else self.leave()

    def load(self):
        assets_dir = self.core.assets_dir
        font = self.core.loader.load_font(assets_dir + 'fonts/GODOFWAR.TTF')
        rollover_sound = self.core.loader.loadSfx(assets_dir + 'sounds/mouse_rollover.wav')
        click_sound = self.core.loader.loadSfx(assets_dir + 'sounds/mouse_click.wav')
        self.return_btn = DirectButton(scale=0.34,
                                       pos=(0, 0, 0.4),
                                       frameColor=(0, 0, 0, 0),
                                       text_font=font,
                                       text_fg=(1, 1, 1, 0.8),
                                       text_pos=(0, -0.05),
                                       text_scale=0.18,
                                       text='Return to game',
                                       image=assets_dir + 'artwork/button.png',
                                       image_scale=(1.1, 1, 0.3),
                                       rolloverSound=rollover_sound,
                                       clickSound=click_sound,
                                       parent=self.node,
                                       command=self.leave)
        self.audio_btn = DirectButton(scale=0.34,
                                      pos=(0, 0, 0.2),
                                      frameColor=(0, 0, 0, 0),
                                      text_font=font,
                                      text_fg=(1, 1, 1, 0.8),
                                      text_pos=(0, -0.05),
                                      text_scale=0.18,
                                      text='Audio settings',
                                      image=assets_dir + 'artwork/button.png',
                                      image_scale=(1.1, 1, 0.3),
                                      rolloverSound=rollover_sound,
                                      parent=self.node,
                                      clickSound=click_sound)
        self.leave_skirmish_btn = DirectButton(scale=0.34,
                                               pos=(0, 0, 0),
                                               frameColor=(0, 0, 0, 0),
                                               text_font=font,
                                               text_fg=(1, 1, 1, 0.8),
                                               text_pos=(0, -0.05),
                                               text_scale=0.18,
                                               text='Leave skirmish',
                                               image=assets_dir + 'artwork/button.png',
                                               image_scale=(1.1, 1, 0.3),
                                               rolloverSound=rollover_sound,
                                               clickSound=click_sound,
                                               parent=self.node,
                                               command=sys.exit)
        self.exit_game_btn = DirectButton(scale=0.34,
                                          pos=(0, 0, -0.2),
                                          frameColor=(0, 0, 0, 0),
                                          text_font=font,
                                          text_fg=(1, 1, 1, 0.8),
                                          text_pos=(0, -0.05),
                                          text_scale=0.18,
                                          text='Exit game',
                                          image=assets_dir + 'artwork/button.png',
                                          image_scale=(1.1, 1, 0.3),
                                          rolloverSound=rollover_sound,
                                          clickSound=click_sound,
                                          parent=self.node,
                                          command=sys.exit)
        self.audio_btn.set_transparency(1)
        self.return_btn.set_transparency(1)
        self.leave_skirmish_btn.set_transparency(1)
        self.exit_game_btn.set_transparency(1)




