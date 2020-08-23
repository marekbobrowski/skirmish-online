from direct.gui.OnscreenImage import OnscreenImage
from direct.actor.Actor import Actor
from panda3d.core import GraphicsOutput
from direct.gui.DirectGui import DirectFrame, DirectEntry, DirectButton, DirectLabel, DirectScrollBar, DGG
from direct.gui.OnscreenText import OnscreenText


class CharacterPreparation:

    def __init__(self, client):
        self.client = client
        self.client.disable_mouse()
        self.client.camera.set_pos(-3.8, -5.8, 1.1)
        self.client.camera.set_h(-50)
        self.client.map.terrain = self.client.loader.load_model('models/terrain.egg')
        self.client.map.terrain.reparent_to(self.client.render)
        self.client.map.tower = self.client.loader.load_model('models/tower.egg')
        self.client.map.tower.reparent_to(self.client.render)
        self.client.map.tower.set_scale(0.5)
        self.client.map.tower.set_pos(5, 5, 0.4)
        self.client.map.tower2 = self.client.loader.load_model('models/tower2.egg')
        self.client.map.tower2.reparent_to(self.client.render)
        self.client.map.tower2.set_scale(0.15)
        self.client.map.tower2.set_pos(-1, -3.5, 0.7)
        self.client.map.tower2.set_h(30)

        rollover_sound = self.client.loader.loadSfx('sounds/mouse_rollover.wav')
        click_sound = self.client.loader.loadSfx('sounds/mouse_click.wav')

        self.knight = Actor("models/knight", {'idle': 'models/animations/knight-Idle',
                                              'run': 'models/animations/knight-Walk',
                                              'attack': 'models/animations/knight-Attack',
                                              'hit': 'models/animations/knight-Hit',
                                              'die': 'models/animations/knight-Die'})
        self.knight.reparent_to(self.client.render)
        self.knight.set_scale(0.05)
        self.knight.set_pos(-2.0, -4.1, 1.11)
        self.knight.set_h(-60)
        self.knight.loop('idle')

        self.priest = Actor("models/priest", {'idle': 'models/animations/priest-Idle',
                                              'run': 'models/animations/priest-Walk',
                                              'attack': 'models/animations/priest-Attack',
                                              'hit': 'models/animations/priest-Hit',
                                              'die': 'models/animations/priest-Die'})
        self.priest.reparent_to(self.client.render)
        self.priest.set_scale(0.035)
        self.priest.set_pos(-2.0, -4.2, 1.0)
        self.priest.set_h(-60)
        self.priest.loop('idle')

        self.archer = Actor("models/archer", {'idle': 'models/animations/archer-Idle',
                                              'run': 'models/animations/archer-Walk',
                                              'attack': 'models/animations/archer-Attack',
                                              'hit': 'models/animations/archer-Hit',
                                              'die': 'models/animations/archer-Die'})
        self.archer.reparent_to(self.client.render)
        self.archer.set_scale(0.035)
        self.archer.set_pos(-2.0, -4.2, 1.11)
        self.archer.set_h(-60)
        self.archer.loop('idle')

        self.mage = Actor("models/mage", {'idle': 'models/animations/mage-Idle',
                                          'run': 'models/animations/mage-Walk',
                                          'attack': 'models/animations/mage-Attack',
                                          'hit': 'models/animations/mage-Hit',
                                          'die': 'models/animations/mage-Die'})
        self.mage.reparent_to(self.client.render)
        self.mage.set_scale(0.035)
        self.mage.set_pos(-1.9, -4.1, 1.1)
        self.mage.set_h(-60)
        self.mage.loop('idle')

        self.priest.hide()
        self.archer.hide()
        self.mage.hide()

        self.client.map.background_image = OnscreenImage(parent=render2dp, image="artwork/map_background.jpg")
        self.client.map.background_image.set_scale(1)
        base.cam2dp.node().getDisplayRegion(0).setSort(-20)
        self.client.main_menu.hide()

        self.warrior_btn = DirectButton(scale=0.34, pos=(-1.5, 0, 0.6), frameColor=(0, 0, 0, 0),
                                        image='artwork/warrior-class.png',
                                        image_scale=0.3,
                                        rolloverSound=rollover_sound,
                                        clickSound=click_sound,
                                        command=self.show_warrior_only)

        self.mage_btn = DirectButton(scale=0.34, pos=(-1.5, 0, 0.3), frameColor=(0, 0, 0, 0),
                                     image='artwork/mage-class.png',
                                     image_scale=0.3,
                                     rolloverSound=rollover_sound,
                                     clickSound=click_sound,
                                     command=self.show_mage_only)

        self.priest_btn = DirectButton(scale=0.34, pos=(-1.5, 0, 0), frameColor=(0, 0, 0, 0),
                                       image='artwork/priest-class.png',
                                       image_scale=0.3,
                                       rolloverSound=rollover_sound,
                                       clickSound=click_sound,
                                       command=self.show_priest_only)

        self.archer_btn = DirectButton(scale=0.34, pos=(-1.5, 0, -0.3), frameColor=(0, 0, 0, 0),
                                       image='artwork/archer-class.png',
                                       image_scale=0.3,
                                       rolloverSound=rollover_sound,
                                       clickSound=click_sound,
                                       command=self.show_archer_only)

        self.choose_class_text = OnscreenText(text='Choose your class', font=self.client.main_menu.logo_font,
                                              pos=(-1, 0.7), scale=0.1)

        self.class_name = OnscreenText(text='Warrior', font=self.client.main_menu.logo_font,
                                       pos=(1, 0.7), scale=0.1, mayChange=True)

        self.player_name_entry = DirectEntry(scale=0.1, pos=(-0.35, 0, -0.9), frameColor=(1, 1, 1, 0.1),
                                             entryFont=self.client.main_menu.ui_font,
                                             width=7)
        self.join_world_btn = DirectButton(scale=0.34, pos=(0.7, 0, -0.7), frameColor=(0, 0, 0, 0),
                                           text_font=self.client.main_menu.logo_font,
                                           text_fg=(1, 1, 1, 0.8), text_pos=(0, -0.05), text_scale=0.18,
                                           text='Join world!', image='textures/button.png',
                                           image_scale=(1.1, 1, 0.3),
                                           rolloverSound=rollover_sound,
                                           clickSound=click_sound)
        self.join_world_btn.set_transparency(1)

    def hide_every_character(self):
        self.priest.hide()
        self.archer.hide()
        self.mage.hide()
        self.knight.hide()

    def show_warrior_only(self):
        self.hide_every_character()
        self.knight.show()

    def show_priest_only(self):
        self.hide_every_character()
        self.priest.show()

    def show_mage_only(self):
        self.hide_every_character()
        self.mage.show()

    def show_archer_only(self):
        self.hide_every_character()
        self.archer.show()
