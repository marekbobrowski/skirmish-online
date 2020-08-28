from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectFrame, DirectEntry, DirectButton, DirectLabel, DirectScrollBar, DGG
from direct.filter.CommonFilters import CommonFilters
from direct.task import Task
import sys
from direct.showbase.Transitions import Transitions
from character_preparation import CharacterPreparation


class Menu:
    def __init__(self, client):
        self.client = client
        self.background = OnscreenImage(parent=render2d, image="artwork/menu_background.jpg")
        self.character_preparation = None

        self.logo_font = client.loader.load_font('fonts/GODOFWAR.TTF')
        self.logo_font.set_pixels_per_unit(100)
        self.ui_font = client.loader.load_font('fonts/Roboto-Condensed.ttf')
        self.ui_font.set_pixels_per_unit(100)

        self.logo_text = OnscreenText(text='Skirmish Online', font=self.logo_font, pos=(0, 0.7), scale=0.2)

        self.ip_entry = DirectEntry(scale=0.1, pos=(-0.35, 0, 0.05), frameColor=(0.7, 0.7, 0.7, 0.4),
                                    entryFont=self.logo_font,
                                    width=7, relief=DGG.RIDGE)
        self.ip_entry.set('127.0.0.1')

        self.rollover_sound = self.client.loader.loadSfx('sounds/mouse_rollover.wav')
        self.click_sound = self.client.loader.loadSfx('sounds/mouse_click.wav')

        self.join_btn = DirectButton(scale=0.34, pos=(0, 0, -0.2), frameColor=(0, 0, 0, 0), text_font=self.logo_font,
                                     text_fg=(1, 1, 1, 0.8), text_pos=(0, -0.05), text_scale=0.18,
                                     text='Join skirmish', image='artwork/button.png',
                                     image_scale=(1.1, 1, 0.3),
                                     rolloverSound=self.rollover_sound,
                                     clickSound=self.click_sound,
                                     command=self.connect_to_server)
        self.join_btn.set_transparency(1)

        self.audio_btn = DirectButton(scale=0.34, pos=(0, 0, -0.45), frameColor=(0, 0, 0, 0), text_font=self.logo_font,
                                      text_fg=(1, 1, 1, 0.8), text_pos=(0, -0.05), text_scale=0.18,
                                      text='Audio settings', image='artwork/button.png',
                                      image_scale=(1.1, 1, 0.3),
                                      rolloverSound=self.rollover_sound,
                                      clickSound=self.click_sound,
                                      command=self.display_audio)
        self.audio_btn.set_transparency(1)

        self.exit_btn = DirectButton(scale=0.34, pos=(0, 0, -0.7), frameColor=(0, 0, 0, 0), text_font=self.logo_font,
                                     text_fg=(1, 1, 1, 0.8), text_pos=(0, -0.05), text_scale=0.18,
                                     text='Exit game', image='artwork/button.png',
                                     image_scale=(1.1, 1, 0.3),
                                     rolloverSound=self.rollover_sound,
                                     clickSound=self.click_sound,
                                     command=lambda: sys.exit())
        self.exit_btn.set_transparency(1)

        self.master_audio_scroll = DirectScrollBar(range=(0, 100), value=50, pageSize=3, orientation=DGG.HORIZONTAL)
        self.master_audio_scroll.set_pos(0, 0, 0.2)

        self.sfx_audio_scroll = DirectScrollBar(range=(0, 100), value=50, pageSize=3, orientation=DGG.HORIZONTAL)
        self.sfx_audio_scroll.set_pos(0, 0, 0)

        self.music_audio_scroll = DirectScrollBar(range=(0, 100), value=50, pageSize=3, orientation=DGG.HORIZONTAL)
        self.music_audio_scroll.set_pos(0, 0, -0.2)

        self.ambiance_audio_scroll = DirectScrollBar(range=(0, 100), value=50, pageSize=3, orientation=DGG.HORIZONTAL)
        self.ambiance_audio_scroll.set_pos(0, 0, -0.4)

        self.back_to_main_btn = DirectButton(scale=0.34, pos=(0, 0, -0.7), frameColor=(0, 0, 0, 0),
                                             text_font=self.logo_font,
                                             text_fg=(1, 1, 1, 0.8), text_pos=(0, -0.05), text_scale=0.18,
                                             text='Return', image='artwork/button.png',
                                             image_scale=(1.1, 1, 0.3),
                                             rolloverSound=self.rollover_sound,
                                             clickSound=self.click_sound,
                                             command=self.display_main)
        self.back_to_main_btn.set_transparency(1)

        self.notification_text = OnscreenText(text='Connecting...', font=self.logo_font, pos=(0, 0), scale=0.15,
                                              mayChange=True)

        self.filters = CommonFilters(client.win, client.cam2d)
        self.filters.setBlurSharpen(0)
        self.client.taskMgr.add(self.fade_in_animation, "SharpenInAnimation")

    def fade_in_animation(self, task):
        amount = task.time
        if amount >= 1:
            self.filters.setBlurSharpen(1)
            self.filters.delBlurSharpen()
            return Task.done
        else:
            self.filters.setBlurSharpen(amount)
        return Task.cont

    def display_main(self):
        self.hide_every_gui_element()
        self.ip_entry.show()
        self.join_btn.show()
        self.audio_btn.show()
        self.exit_btn.show()
        self.logo_text.show()
        self.background.show()

    def hide_every_gui_element(self):
        self.ip_entry.hide()
        self.join_btn.hide()
        self.audio_btn.hide()
        self.exit_btn.hide()
        self.master_audio_scroll.hide()
        self.sfx_audio_scroll.hide()
        self.music_audio_scroll.hide()
        self.ambiance_audio_scroll.hide()
        self.back_to_main_btn.hide()
        self.notification_text.hide()

    def hide(self):
        self.hide_every_gui_element()
        self.logo_text.hide()
        self.background.hide()

    def display_audio(self):
        self.hide_every_gui_element()
        self.master_audio_scroll.show()
        self.sfx_audio_scroll.show()
        self.music_audio_scroll.show()
        self.ambiance_audio_scroll.show()
        self.back_to_main_btn.show()

    def connect_to_server(self):
        self.display_notification("Connecting...")
        if self.client.network_manager.connect(self.ip_entry.get()):
            self.display_notification("Connected!\nLoading models...")
            self.load_character_preparation()
        else:
            self.display_notification('Failed to connect.')
            self.back_to_main_btn.show()

    def display_notification(self, text):
        self.hide_every_gui_element()
        self.logo_text.show()
        self.background.show()
        self.notification_text.setText(text)
        self.notification_text.show()
        self.client.graphicsEngine.render_frame()
        self.client.graphicsEngine.render_frame()
        self.client.graphicsEngine.render_frame()

    def load_character_preparation(self):
        if self.character_preparation is None:
            self.character_preparation = CharacterPreparation(self.client)
        else:
            self.client.menu.hide()
            self.character_preparation.show()