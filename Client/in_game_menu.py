from direct.gui.DirectGui import DirectButton
import sys

class InGameMenu:
    def __init__(self, client):
        self.client = client
        self.return_btn = DirectButton(scale=0.34, pos=(0, 0, 0.4), frameColor=(0, 0, 0, 0),
                                       text_font=self.client.menu.logo_font,
                                       text_fg=(1, 1, 1, 0.8), text_pos=(0, -0.05), text_scale=0.18,
                                       text='Return to game', image='artwork/button.png',
                                       image_scale=(1.1, 1, 0.3),
                                       rolloverSound=self.client.menu.rollover_sound,
                                       clickSound=self.client.menu.click_sound,
                                       command=lambda: self.client.in_game_menu.hide())
        self.audio_btn = DirectButton(scale=0.34, pos=(0, 0, 0.2), frameColor=(0, 0, 0, 0),
                                      text_font=self.client.menu.logo_font,
                                      text_fg=(1, 1, 1, 0.8), text_pos=(0, -0.05), text_scale=0.18,
                                      text='Audio settings', image='artwork/button.png',
                                      image_scale=(1.1, 1, 0.3),
                                      rolloverSound=self.client.menu.rollover_sound,
                                      clickSound=self.client.menu.click_sound,
                                      command=self.client.menu.display_audio)
        self.back_to_main_menu_btn = DirectButton(scale=0.34, pos=(0, 0, 0), frameColor=(0, 0, 0, 0),
                                                  text_font=self.client.menu.logo_font,
                                                  text_fg=(1, 1, 1, 0.8), text_pos=(0, -0.05), text_scale=0.18,
                                                  text='Logout', image='artwork/button.png',
                                                  image_scale=(1.1, 1, 0.3),
                                                  rolloverSound=self.client.menu.rollover_sound,
                                                  clickSound=self.client.menu.click_sound,
                                                  command=self.logout)
        self.exit_game_btn = DirectButton(scale=0.34, pos=(0, 0, -0.2), frameColor=(0, 0, 0, 0),
                                          text_font=self.client.menu.logo_font,
                                          text_fg=(1, 1, 1, 0.8), text_pos=(0, -0.05), text_scale=0.18,
                                          text='Exit game', image='artwork/button.png',
                                          image_scale=(1.1, 1, 0.3),
                                          rolloverSound=self.client.menu.rollover_sound,
                                          clickSound=self.client.menu.click_sound,
                                          command=self.exit_game)
        self.audio_btn.set_transparency(1)
        self.return_btn.set_transparency(1)
        self.back_to_main_menu_btn.set_transparency(1)
        self.exit_game_btn.set_transparency(1)
        self.is_hidden = True
        self.hide()

    def show(self):
        self.audio_btn.show()
        self.return_btn.show()
        self.back_to_main_menu_btn.show()
        self.exit_game_btn.show()
        self.is_hidden = False

    def hide(self):
        self.audio_btn.hide()
        self.return_btn.hide()
        self.back_to_main_menu_btn.hide()
        self.exit_game_btn.hide()
        self.is_hidden = True

    def logout(self):
        self.client.network_manager.disconnect()
        self.client.ignore_all()
        self.client.world.hide()
        self.client.in_game_menu.hide()
        self.client.menu.display_main()

    def exit_game(self):
        self.client.network_manager.disconnect()
        sys.exit()




