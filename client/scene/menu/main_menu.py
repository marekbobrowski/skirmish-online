from direct.gui.DirectGui import DirectEntry, DirectButton, DGG
import sys
import assets_dir_config
from scene.menu import connect


# noinspection PyArgumentList
class MainMenu:
    def __init__(self, parent):
        self.parent = parent
        self.node = parent.node.attach_new_node("Main-Menu Node")
        self.connecting = False
        self.node.hide()

        # Main menu graphical/sound/input components
        self.ip_entry = None
        self.connect_btn = None
        self.audio_btn = None
        self.exit_btn = None
        self.notification_text = None

    def load(self):
        assets_dir = assets_dir_config.assets_dir

        # Ip entry
        self.ip_entry = DirectEntry(scale=0.1,
                                    pos=(-0.35, 0, 0.05),
                                    frameColor=(0.7, 0.7, 0.7, 0.4),
                                    entryFont=self.parent.font,
                                    width=7,
                                    relief=DGG.RIDGE,
                                    parent=self.node)
        self.ip_entry.set('127.0.0.1')
        # Buttons
        self.connect_btn = DirectButton(scale=0.34, pos=(0, 0, -0.2),
                                        frameColor=(0, 0, 0, 0),
                                        text_font=self.parent.font,
                                        text_fg=(1, 1, 1, 0.8),
                                        text_pos=(0, -0.05),
                                        text_scale=0.18,
                                        text='Connect',
                                        image=assets_dir + 'artwork/button.png',
                                        parent=self.node,
                                        image_scale=(1.1, 1, 0.3),
                                        rolloverSound=self.parent.rollover_sound,
                                        clickSound=self.parent.click_sound,
                                        command=lambda: connect.connect_attempt(self.ip_entry.get()))
        self.connect_btn.set_transparency(1)
        self.audio_btn = DirectButton(scale=0.34, pos=(0, 0, -0.45),
                                      frameColor=(0, 0, 0, 0),
                                      text_font=self.parent.font,
                                      text_fg=(1, 1, 1, 0.8),
                                      text_pos=(0, -0.05),
                                      text_scale=0.18,
                                      text='Audio settings',
                                      image=assets_dir + 'artwork/button.png',
                                      parent=self.node,
                                      image_scale=(1.1, 1, 0.3),
                                      rolloverSound=self.parent.rollover_sound,
                                      clickSound=self.parent.click_sound,
                                      command=lambda: self.parent.change_subscene_to(1))
        self.audio_btn.set_transparency(1)
        self.exit_btn = DirectButton(scale=0.34,
                                     pos=(0, 0, -0.7),
                                     frameColor=(0, 0, 0, 0),
                                     text_font=self.parent.font,
                                     text_fg=(1, 1, 1, 0.8),
                                     text_pos=(0, -0.05),
                                     text_scale=0.18,
                                     parent=self.node,
                                     text='Exit game',
                                     image=assets_dir + 'artwork/button.png',
                                     image_scale=(1.1, 1, 0.3),
                                     rolloverSound=self.parent.rollover_sound,
                                     clickSound=self.parent.click_sound,
                                     command=lambda: sys.exit())
        self.exit_btn.set_transparency(1)

    def enter(self):
        self.node.show()

    def leave(self):
        self.node.hide()



