from direct.gui.DirectGui import DirectEntry, DirectButton, DGG
import sys
from threading import Thread


class MainMenu:
    def __init__(self, menu):
        self.menu = menu
        self.main_menu_node = menu.menu_node.attach_new_node("Main-Main Node")
        self.connecting = False
        self.main_menu_node.hide()

        # Main menu graphical/sound/input components
        self.ip_entry = None
        self.connect_btn = None
        self.audio_btn = None
        self.exit_btn = None
        self.notification_text = None

    def load(self):
        assets_dir = self.menu.core.assets_dir

        # Ip entry
        self.ip_entry = DirectEntry(scale=0.1,
                                    pos=(-0.35, 0, 0.05),
                                    frameColor=(0.7, 0.7, 0.7, 0.4),
                                    entryFont=self.menu.font,
                                    width=7,
                                    relief=DGG.RIDGE,
                                    parent=self.main_menu_node)
        self.ip_entry.set('127.0.0.1')
        # Buttons
        self.connect_btn = DirectButton(scale=0.34, pos=(0, 0, -0.2),
                                        frameColor=(0, 0, 0, 0),
                                        text_font=self.menu.font,
                                        text_fg=(1, 1, 1, 0.8),
                                        text_pos=(0, -0.05),
                                        text_scale=0.18,
                                        text='Connect',
                                        image=assets_dir + 'artwork/button.png',
                                        parent=self.main_menu_node,
                                        image_scale=(1.1, 1, 0.3),
                                        rolloverSound=self.menu.rollover_sound,
                                        clickSound=self.menu.click_sound,
                                        command=self.connect_attempt)
        self.connect_btn.set_transparency(1)
        self.audio_btn = DirectButton(scale=0.34, pos=(0, 0, -0.45),
                                      frameColor=(0, 0, 0, 0),
                                      text_font=self.menu.font,
                                      text_fg=(1, 1, 1, 0.8),
                                      text_pos=(0, -0.05),
                                      text_scale=0.18,
                                      text='Audio settings',
                                      image=assets_dir + 'artwork/button.png',
                                      parent=self.main_menu_node,
                                      image_scale=(1.1, 1, 0.3),
                                      rolloverSound=self.menu.rollover_sound,
                                      clickSound=self.menu.click_sound,
                                      command=lambda: self.menu.change_subscene_to(1))
        self.audio_btn.set_transparency(1)
        self.exit_btn = DirectButton(scale=0.34,
                                     pos=(0, 0, -0.7),
                                     frameColor=(0, 0, 0, 0),
                                     text_font=self.menu.font,
                                     text_fg=(1, 1, 1, 0.8),
                                     text_pos=(0, -0.05),
                                     text_scale=0.18,
                                     parent=self.main_menu_node,
                                     text='Exit game',
                                     image=assets_dir + 'artwork/button.png',
                                     image_scale=(1.1, 1, 0.3),
                                     rolloverSound=self.menu.rollover_sound,
                                     clickSound=self.menu.click_sound,
                                     command=lambda: sys.exit())
        self.exit_btn.set_transparency(1)

    def enter(self):
        self.main_menu_node.show()
        print('DEBUG: entered main-menu')

    def leave(self):
        self.main_menu_node.hide()
        print('DEBUG: left main-menu')

    def connect_attempt(self):
        if not self.connecting:
            self.connecting = True
            # running this function in new thread so connecting & model loading don't block the main thread
            Thread(target=self.connect).start()

    def connect(self):
        self.menu.scene_manager.show_dialog('Connecting...')
        server_ip = self.ip_entry.get()
        connected = self.menu.core.network_manager.connect(server_ip)
        if connected:
            self.menu.scene_manager.show_dialog('Connected! Loading models...')
            self.menu.scene_manager.load_scene(1)
            self.menu.scene_manager.change_scene_to(1)
            self.menu.scene_manager.hide_dialog()
        else:
            self.menu.scene_manager.show_dialog('Failed to connect.')
        self.connecting = False

